import json
import datetime

import requests
from flask import Flask, jsonify, send_from_directory, abort, g
from flask import request
from flask.ext.httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from passlib.apps import custom_app_context as pwd_context


app = Flask(__name__, static_url_path="")
app.config.from_pyfile('stats.cfg')
db = SQLAlchemy(app)
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


db.create_all()
