import os
import json
from flask import jsonify, redirect, url_for
from flask import request, send_from_directory
from api import app
from api.users import verify_auth_token
from api.utils import spcall
from api.utils import build_json, clean_form
from api.utils import InvalidForm, DuplicateRow, InvalidRequest
from api.users import user_exists, generate_auth_token
from passlib.apps import custom_app_context as pwd_context
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "OK", "message": "OK"})


# Users

@auth.verify_password
def verify_password(username_or_token, password):
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        try:
            hashed_password = spcall("getpassword", (username_or_token,))[0][0]
            verified = pwd_context.verify(password, hashed_password)
            if not verified:
                return False
        except:
            return False

    # request.authorization.username = user
    return True


@app.route('/auth/', methods=['POST'])
def auth_user():
    data = json.loads(request.data)
    if clean_form(data):
        user = spcall('getusername', (data['username'],))[0][0]

        if user == None:
            return jsonify({"status": "error", "message": "Invalid username/password"}), 404
        else:
            if verify_password(data['username'], data['password']):
                token = generate_auth_token(data['username'])
                return jsonify({"token": token})
            return jsonify({"status": "error", "message": "Invalid username/password"}), 404
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/register/', methods=['POST'])
def register_user():
    data = json.loads(request.data)  # Now that we know the password won't be null, then we check if user exists

    if user_exists(data['username']):
        raise DuplicateRow('Already exists', status_code=422)

    password = pwd_context.encrypt(data['password'])

    response = spcall('users_upsert', (
        None,
        data['username'],
        data['email'],
        password,
        str(data['date_created']),
        data['is_admin'],), True)

    json_dict = build_json(response)

    return jsonify(json_dict), 201


@app.route('/token/')
@auth.login_required
def get_auth_token():
    username = request.authorization.username
    token = generate_auth_token(username)
    return jsonify({'token': token.decode('ascii')})


@app.route('/upload/', methods=["POST"])
def upload_photo():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({"status": "OK"})


@app.route('/uploads/<filename>', methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/token/status/', methods=["POST"])
def get_auth_token_status():
    try:
        data = json.loads(request.data)
        token = data['token']
        validToken = verify_auth_token(token)
        if validToken:
            return jsonify({"status": "OK", "user": validToken})
    except:
        return jsonify({"status": "error"})
    return jsonify({"status": "error"})


# Products

@app.route('/products/', methods=['GET'])
@app.route('/products/<product_id>/', methods=['GET'])
def products_get(product_id=None):
    data = spcall('products_get', (product_id,), )
    response = build_json(data)

    if product_id and len(response['entries']) == 0:
        """ Product ID does not exist """
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(response)


# @app.route('/merchants/', methods=['GET'])
# @app.route('/merchants/<merchant_id>/', methods=['GET'])
# @auth.login_required
# def merchants_get(merchant_id=None):
#     items = build_json(spcall('merchants_get', (merchant_id,), ))
#     return jsonify(items)

@app.route('/merchants/', methods=['GET'])
@app.route('/merchants/<merchant_username>/', methods=['GET'])
# @auth.login_required
def merchants_get(merchant_username=None):
    items = build_json(spcall('merchants_get', (merchant_username,), ))
    return jsonify(items)


@app.route('/products/', methods=['POST'])
@app.route('/products/<product_id>/', methods=['PUT'])
@auth.login_required
def products_upsert(product_id=None):
    data = json.loads(request.data)

    # Everything should be clean except id in post
    if clean_form(data):
        response = spcall('products_upsert', (
            product_id,
            data['merchant_id'],
            data['thumb_url'],
            data['title'],
            data['long_description'],
            data['sku'],
            data['short_description'],
            data['stock_on_hand'],
            data['unit_selling_cost'],
            data['category_id'],
            str(data['date_added']),
            data['is_active'],
            data['is_featured'],), True)
        print response
        # If it is an update, then raise an 404 error if id doesn't exist
        if product_id and response[0][0] == 'error' and request.method == "PUT":
            raise InvalidRequest('Does not exist', status_code=404)

        json_dict = build_json(response)

        status_code = 200
        if not product_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/merchants/', methods=['POST'])
@app.route('/merchants/<merchant_id>/', methods=['PUT'])
# @auth.login_required
def merchants_upsert(merchant_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('merchants_upsert', (
            merchant_id,
            data['user_id'],
            data['shop_name'],
            data['merchant_name'],
            data['logo_url'],
            str(data['date_created']),), True)
        json_dict = build_json(response)

        status_code = 200
        if not merchant_id:
            status_code = 201

        return jsonify(json_dict), status_code  # Item Attributes
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/products/<product_id>/attributes/', methods=['GET'])
@app.route('/products/<product_id>/attributes/<attribute_id>/', methods=['GET'])
def product_attributes_get(product_id, attribute_id=None):
    response = spcall('product_attributes_get', (attribute_id, product_id,), )

    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/products/<product_id>/attributes/', methods=['POST'])
@app.route('/products/<product_id>/attributes/<attribute_id>/', methods=['PUT'])
@auth.login_required
def product_attributes_upsert(product_id, attribute_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('product_attributes_upsert', (
            data['attribute_value'],
            data['attribute_id'],
            data['product_id'],
        ), True)

        json_dict = build_json(response)

        status_code = 200
        if not attribute_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)  # Images


@app.route('/products/<product_id>/tags/', methods=['GET'])
@app.route('/products/<product_id>/tags/<tag_id>/', methods=['GET'])
def product_tags_get(product_id, tag_id=None):
    response = spcall('product_tags_get', (product_id, tag_id,), )

    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/products/<product_id>/tags/', methods=['POST'])
@app.route('/products/<product_id>/tags/<tag_id>/', methods=['PUT'])
@auth.login_required
def product_tags_upsert(product_id, tag_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('product_tags_upsert', (
            int(data['product_id']),
            int(data['tag_id']),
        ), True)

        json_dict = build_json(response)

        status_code = 200
        if not tag_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)  # Images


@app.route('/products/<item_id>/images/', methods=['POST'])
@app.route('/products/<item_id>/images/<image_id>/', methods=['PUT'])
def product_images_upsert(item_id, image_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('product_images_upsert', (
            image_id,
            data['product_id'],
            data['image'],
            data['caption'],), True)

        json_dict = build_json(response)

        status_code = 200
        if not image_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)  # Images


@app.route('/categories/<item_id>/images/', methods=['POST'])
@app.route('/categories/<item_id>/images/<image_id>/', methods=['PUT'])
def category_images_upsert(item_id, image_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('category_images_upsert', (
            image_id,
            data['category_id'],
            data['image'],
            data['caption'],), True)

        json_dict = build_json(response)

        status_code = 200
        if not image_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)  # Images


# Attributes

@app.route('/attributes/', methods=['GET'])
@app.route('/attributes/<attribute_id>/', methods=['GET'])
@auth.login_required
def attributes_get(attribute_id=None):
    response = spcall('attributes_get', (attribute_id,))

    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/attributes/', methods=['POST'])
@app.route('/attributes/<attribute_id>/', methods=['PUT'])
def attributes_upsert(attribute_id=None):
    data = json.loads(request.data)

    if clean_form(data):

        response = spcall('attributes_upsert', (
            attribute_id,
            data['attribute_name'],
            data['validation'],), True)

        json_dict = build_json(response)

        status_code = 200
        if not attribute_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/tags/', methods=['GET'])
@app.route('/tags/<tag_id>/', methods=['GET'])
@auth.login_required
def tags_get(tag_id=None):
    response = spcall('tags_get', (tag_id,))

    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/tags/', methods=['POST'])
@app.route('/tags/<tag_id>/', methods=['PUT'])
def tags_upsert(tag_id=None):
    data = json.loads(request.data)

    if clean_form(data):

        response = spcall('tags_upsert', (
            tag_id,
            data['name'],
            data['slug'],), True)

        json_dict = build_json(response)

        status_code = 200
        if not tag_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


# Customers

@app.route('/customers/', methods=['GET'])
@app.route('/customers/<customer_id>/', methods=['GET'])
@auth.login_required
def customers_get(customer_id=None):
    response = spcall('customers_get', (customer_id,), )
    json_dict = build_json(response)

    return jsonify(json_dict)


# Product Categories

@app.route('/categories/', methods=['GET'])
@app.route('/categories/<category_id>/', methods=['GET'])
def categories_get(category_id=None):
    response = spcall('categories_get', (category_id,), )
    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/categories/<category_id>/products/', methods=['GET'])
@app.route('/categories/<category_id>/products/<product_id>', methods=['GET'])
def products_in_categories_get(category_id, product_id=None):
    response = spcall('products_in_categories_get', (category_id, product_id,), )
    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/categories/<category_id>/', methods=['PUT'])
@app.route('/categories/', methods=['POST'])
@auth.login_required
def categories_upsert(category_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('categories_upsert', (
            category_id,
            data['name'],
            data['slug'],
            data['parent'],
            data['description'],
            data['is_active'],), True)
        json_dict = build_json(response)

        status_code = 200
        if not category_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/customers/<customer_id>/', methods=['PUT'])
@app.route('/customers/', methods=['POST'])
@auth.login_required
def customers_upsert(customer_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('customers_upsert', (
            customer_id,
            data['user_id'],
            data['name'],
            data['billing_address'],
            data['shipping_address'],
            data['date_created'],), True)
        json_dict = build_json(response)

        status_code = 200
        if not customer_id:
            status_code = 201

        return jsonify(json_dict), status_code
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


# Users

@app.route('/users/', methods=['GET'])
@app.route('/users/<user_id>/', methods=['GET'])
@auth.login_required
def users_get(user_id=None):
    # User id is used to query
    if user_id and user_id.isdigit():
        response = spcall('users_get', (user_id,), )
        return jsonify(build_json(response))

    # Username is used to query
    if user_id:
        response = spcall('users_username_get', (user_id,), )
        return jsonify(build_json(response))

    # Query all
    response = spcall('users_get', (user_id,), )
    return jsonify(build_json(response))


@app.route('/users/', methods=['POST'])
@app.route('/users/<user_id>/', methods=['PUT'])
@auth.login_required
def users_upsert(user_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        # Now that we know the password won't be null, then we check if user exists
        if user_exists(data['username']) and not user_id:
            raise DuplicateRow('Already exists', status_code=422)

        password = pwd_context.encrypt(data['password'])

        response = spcall('users_upsert', (
            user_id,
            data['username'],
            data['email'],
            password,
            str(data['date_created']),
            data['is_admin'],), True)

        json_dict = build_json(response)

        status_code = 200
        if not user_id:
            status_code = 201

        return jsonify(json_dict), status_code

    else:
        raise InvalidForm('Some fields have error values', status_code=422)


# Wishlists and Items

@app.route('/wishlists/', methods=['POST'])
@app.route('/wishlists/<wishlist_id>/', methods=['PUT'])
@auth.login_required
def wishlists_upsert(wishlist_id=None):
    data = json.loads(request.data)

    response = spcall('wishlists_upsert', (
        wishlist_id,
        data['wishlist_name'],), True)

    json_dict = build_json(response)

    status_code = 200
    if not wishlist_id:
        status_code = 201

    return jsonify(json_dict), status_code


@app.route('/wishlists/<wishlist_id>/items/', methods=['POST'])
@app.route('/wishlists/<wishlist_id>/items/<item_id>/', methods=['PUT'])
@auth.login_required
def wishlist_items_upsert(wishlist_id, item_id=None):
    data = json.loads(request.data)

    response = spcall('wishlist_items_upsert', (
        data['wishlist_id'],
        data['product_id'],
        str(data['time_stamp']),), True)

    json_dict = build_json(response)

    status_code = 200
    if not item_id:
        status_code = 201

    return jsonify(json_dict), status_code


@app.route('/wishlists/', methods=['GET'])
@app.route('/wishlists/<wishlist_id>/', methods=['GET'])
@auth.login_required
def wishlist_get(wishlist_id=None):
    response = spcall('wishlists_get', (wishlist_id,), )

    json_dict = build_json(response)

    return jsonify(json_dict)


@app.route('/wishlists/<wishlist_id>/items/', methods=['GET'])
@app.route('/wishlists/<wishlist_id>/items/<item_id>/', methods=['GET'])
@auth.login_required
def wishlist_items_get(wishlist_id, item_id=None):
    response = spcall('wishlist_items_get', (wishlist_id, item_id), )

    json_dict = build_json(response)

    return jsonify(json_dict)


# Cart and Items


@app.route('/carts/<cart_id>/items/', methods=['POST'])
@auth.login_required
def cart_items_new(cart_id):
    data = json.loads(request.data)

    response = spcall('cart_items_new', (
        data['cart_id'],
        data['product_id'],
        data['quantity'],
        str(data['time_stamp']),), True)

    json_dict = build_json(response)

    return jsonify(json_dict), 201


@app.route('/carts/<cart_id>/items/', methods=['GET'])
@app.route('/carts/<cart_id>/items/<item_id>/', methods=['GET'])
@auth.login_required
def cart_items_get(cart_id, item_id=None):
    response = spcall('cart_items_get', (cart_id, item_id,))
    json_dict = build_json(response)

    if item_id and len(json_dict['entries']) == 0:
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(json_dict)


# Cart and Items

@app.route('/carts/', methods=['POST'])
@auth.login_required
def carts_new():
    data = json.loads(request.data)
    response = spcall('carts_new', (
        data['session_id'],
        str(data['date_created']),
        data['customer_id'],
        data['is_active'],), True)

    json_dict = build_json(response)

    return jsonify(json_dict), 201


@app.route('/carts/<cart_id>/', methods=['GET'])
@app.route('/carts/', methods=['GET'])
@auth.login_required
def carts_get(cart_id=None):
    response = spcall('carts_get', (cart_id,))

    json_dict = build_json(response)
    if cart_id and len(json_dict['entries']) == 0:
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(json_dict)


# Orders and Items

@app.route('/orders/', methods=['POST'])
@auth.login_required
def orders_new():
    data = json.loads(request.data)

    response = spcall('orders_new', (
        data['customer_id'],
        str(data['date_ordered']),
        data['status'],
        data['reference_no'],
        data['total_amount'],), True)

    if 'Error' in str(response[0][0]):
        return jsonify({'status': 'error', 'message': response[0][0]})

    return jsonify({'status': 'OK', 'message': response[0][0]}), 201


@app.route('/orders/<order_id>/', methods=['GET'])
@app.route('/orders/', methods=['GET'])
@auth.login_required
def orders_get(order_id=None):
    response = spcall('orders_get', (order_id,))

    json_dict = build_json(response)

    if order_id and len(json_dict['entries']) == 0:
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(json_dict)


@app.route('/orders/<order_id>/items/', methods=['GET'])
@app.route('/orders/<order_id>/items/<item_id>/', methods=['GET'])
@auth.login_required
def order_items_get(order_id, item_id=None):
    response = spcall('order_items_get', (order_id, item_id))

    json_dict = build_json(response)

    if item_id and len(json_dict['entries']) == 0:
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(json_dict)


@app.route('/orders/<order_id>/items/', methods=['POST'])
@auth.login_required
def order_items_new(order_id):
    data = json.loads(request.data)

    response = spcall('order_items_new', (
        order_id,
        data['product_id'],
        data['quantity'],), True)

    if 'Error' in response[0][0]:
        return jsonify({'status': 'error', 'message': response[0][0]})

    return jsonify({'status': 'OK', 'message': response[0][0]}), 201


# Suppliers

@app.route('/suppliers/', methods=['POST'])
@auth.login_required
def suppliers_new(supplier_id=None):
    data = json.loads(request.data)

    if clean_form(data):
        response = spcall('suppliers_new', (
            data['name'],
            data['address'],
            data['phone'],
            data['fax'],
            data['email'],
            data['is_active'],), True)

        if 'Error' in response[0][0]:
            return jsonify({'status': 'error', 'message': response[0][0]})

        return jsonify({'status': 'OK', 'message': response[0][0]}), 201
    else:
        raise InvalidForm('Some fields have error values', status_code=422)


@app.route('/suppliers/', methods=['GET'])
@app.route('/suppliers/<supplier_id>/', methods=['GET'])
@auth.login_required
def suppliers_get(supplier_id=None):
    response = spcall('suppliers_get', (supplier_id,))
    json_dict = build_json(response)

    if supplier_id and len(json_dict['entries']) == 0:
        raise InvalidRequest('Does not exist', status_code=404)

    return jsonify(json_dict)
