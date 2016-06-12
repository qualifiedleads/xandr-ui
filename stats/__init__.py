import json
import datetime

import requests
from flask import Flask, jsonify, send_from_directory, abort, g
from flask import request
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__, static_url_path="")
app.config.from_pyfile('stats.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost/rtbstats'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
auth = HTTPBasicAuth()



class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(200))
    email = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    date_added = db.Column(db.DateTime)

    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    user_type = db.relationship('UserType', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, first_name, last_name, user_type=None, state=True, phone=None, date_added=None):
        self.phone = phone
        self.last_name = last_name
        self.first_name = first_name
        self.state = state
        self.user_type = user_type
        self.username = username
        self.email = email
        if date_added is None:
            date_added = datetime.datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Category(db.Model):
    #https://wiki.appnexus.com/display/api/Category+Service
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_sensitive = db.Column(db.Boolean)
    requires_whitelist = db.Column(db.Boolean)
    requires_whitelist = db.Column(db.Boolean)
    requires_whitelist_on_external = db.Column(db.Boolean)
    last_modified = db.Column(db.TIMESTAMP)
    is_brand_eligible = db.Column(db.Boolean)
    #countries_and_brands = db.Column(db.String) #array of objects !!! need to look at data returned by API ! it is a mess! See the model BrandInCountry below

class Brand(db.Model):
    #https://wiki.appnexus.com/display/api/Brand+Service
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    urls = db.Column(db.String) #array is needed ????
    is_premium = db.Column(db.Boolean)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    company_id = db.Column(db.Integer) #FK is needed in future
    num_creatives = db.Column(db.Integer)
    last_modified = db.Column(db.String)

class Country(db.Model):
    #https://wiki.appnexus.com/display/api/Country+Service
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String) #enum in origin

class BrandInCountry(db.Model):
    #See the model Category.countries_and_brands
    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class Advertiser(db.Model):
    #https://wiki.appnexus.com/display/api/Advertiser+Service
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String)
    name = db.Column(db.String)
    state = db.Column(db.Enum('active', 'inactive', name='advartiser_states'))
    default_brand_id = db.Column(db.Integer)
    remarketing_segment_id = db.Column(db.Integer)
    lifetime_budget = db.Column(db.Float)
    lifetime_budget_imps = db.Column(db.Integer)
    daily_budget = db.Column(db.Float)
    daily_budget_imps = db.Column(db.Integer)
    #competitive_brands #see model AdvertiserBrands below
    #competitive_categories	#see model AdvertiserCategories below
    enable_pacing = db.Column(db.Boolean)
    allow_safety_pacing = db.Column(db.Boolean)
    profile_id = db.Column(db.Integer)
    control_pct = db.Column(db.Float)
    timezone = db.Column(db.String) #originally it is enum
    last_modified = db.Column(db.TIMESTAMP)
    #stats	object #should be in sepparait model if needed
    #billing_internal_user	array
    billing_name = db.Column(db.String)
    billing_phonee = db.Column(db.String)
    billing_address1 = db.Column(db.String)
    billing_address2 = db.Column(db.String)
    billing_city = db.Column(db.String)
    billing_state = db.Column(db.String)
    billing_country	= db.Column(db.String)
    billing_zip	= db.Column(db.String)
    default_currency = db.Column(db.String)
    default_category = db.Column(db.String) #object in origin - no description! need to see real data
    #labels	array - see model AdvertiserLabels below
    use_insertion_orders = db.Column(db.Boolean)
    time_format = db.Column(db.Enum('12-hour', '24-hour', name='time_formats'))
    default_brand_id = db.Column(db.Integer, db.ForeignKey('brand.id')) #default_brand in origin API responce
    is_mediated = db.Column(db.Boolean)
    is_malicious = db.Column(db.Boolean)
    #object_stats	object #should be in sepparait model if needed
    #thirdparty_pixels	array # see the model AdvertiserThirdpartyPixels below

class AdvertiserBrands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))

class AdvertiserCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

class AdvertiserLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label_type_id = db.Column(db.Integer, db.ForeignKey('label_type.id')) #id in origin
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    name = db.Column(db.Enum('Salesperson', 'Account Manager', 'Advertiser Type', name='label_types'))
    value = db.Column(db.String)

class AdvertiserThirdpartyPixels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    thirdparty_pixel_id = db.Column(db.Integer, db.ForeignKey('thirdparty_pixel.id'))

class ThirdPartyPixel(db.Model):
    #https://wiki.appnexus.com/display/api/Third-Party+Pixel+Service
    #TODO need to be continued
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    name = db.Column(db.String)

def apn_service_headers():
    # TODO: Place in environment variable
    auth_url = "https://api.appnexus.com/auth"
    data = {"auth": {"username": "stats_api", "password": "API?1nsid3!"}}
    auth_request = requests.post(auth_url, data=json.dumps(data))
    response = json.loads(auth_request.content)

    try:
        token = response['response']['token']
    except:
        token = ''

    headers = {"Authorization": token, 'Content-Type': 'application/json'}

    return headers


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route("/")
def index():
    return send_from_directory('static', 'index.html')


# Appnexus API Endpoints
@app.route("/appnexus/reports/")
def network_analytics():
    return jsonify({"data": ""})


@app.route("/appnexus/users/", methods=['GET'])
@auth.login_required
def users_appnexus_get():
    headers = apn_service_headers()
    r = requests.get('https://api.appnexus.com/user', headers=headers)
    response = json.loads(r.content)
    return jsonify(response)


# Caravel API Endpoints
@app.route("/caravel/users/", methods=['GET'])
def users_caravel_get():
    users = User.query.all()
    return jsonify({"results": users})


@app.route("/caravel/users/", methods=['POST'])
def users_create():
    print "Saving"

    username = request.json.get('username')
    email = request.json.get('email')
    first_name = request.json.get('first_name')
    password = request.json.get('password')
    last_name = request.json.get('last_name')

    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user

    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201


#db.create_all()
if __name__ == '__main__':
    manager.run()
