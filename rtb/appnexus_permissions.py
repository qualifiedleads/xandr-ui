import requests
from django.conf import settings
from models import FrameworkUser, User, UserAdvertiserAccess
from report import get_auth_token
import json

appnexus_url = settings.__dict__.get(
    'APPNEXUS_URL', 'https://api.appnexus.com/')

def load_appnexus_permissions(user_id):
    try:
        url = appnexus_url + User.api_endpoint
        token = get_auth_token()
        r = requests.get(
            url, params={'id':user_id}, headers={
                "Authorization": token})
        response = json.loads(r.content)['response']
        user = response['user']
        rights=user["advertiser_access"] or [user['advertiser_id']]
        objs=map(lambda x:UserAdvertiserAccess(user_id=user_id,advertiser_id=x),
                 filter(None, rights))
        UserAdvertiserAccess.objects.filter(user_id=user_id).delete()
        UserAdvertiserAccess.objects.bulk_save(objs)

    except Exception as e:
        print 'In func "load_appnexus_permissions" raised error:',e
