import json
import os
import requests
from flask import Flask, jsonify, send_from_directory
from flask import render_template, request

app = Flask(__name__, static_url_path="")
app.config.from_pyfile('api.cfg')


@app.route("/")
def index():
    return send_from_directory('static', 'index.html')


@app.route("/network_analytics")
def network_analytics():
    return jsonify({"data": ""})
