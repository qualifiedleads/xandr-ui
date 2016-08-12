import requests
from django.conf import settings
from models import FrameworkUser,User
from report import get_auth_token
import json

appnexus_url = settings.__dict__.get(
    'APPNEXUS_URL', 'https://api.appnexus.com/')

def load_appnexus_permissions(user_id):
    url = appnexus_url + User.api_endpoint
    token = get_auth_token()
    r = requests.get(
        url, params={'id':user_id}, headers={
            "Authorization": token})
    response = json.loads(r.content)['response']

