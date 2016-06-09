import json
import os
import requests
import datetime
from flask import Flask, jsonify, send_from_directory
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="")
app.config.from_pyfile('stats.cfg')
db = SQLAlchemy(app)


class UserType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    phone = db.Column(db.String(80))
    date_added = db.Column(db.DateTime)

    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'))
    user_type = db.relationship('UserType', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, state, username, password, email, first_name, last_name, phone, user_type, date_added=None):
        self.phone = phone
        self.last_name = last_name
        self.first_name = first_name
        self.password = password
        self.state = state
        self.user_type = user_type
        self.username = username
        self.email = email
        if date_added is None:
            date_added = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % self.username


def apn_service_headers():
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


@app.route("/")
def index():
    return send_from_directory('static', 'index.html')


@app.route("/network_analytics")
def network_analytics():
    return jsonify({"data": ""})


@app.route("/users")
def users_get():
    results = []

    headers = apn_service_headers()
    r = requests.get('https://api.appnexus.com/user', headers=headers)

    out = json.loads(r.content)

    print out

    return jsonify({"results": results})
