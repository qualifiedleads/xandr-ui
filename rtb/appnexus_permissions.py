import requests
from django.conf import settings
from models import FrameworkUser, User, UserAdvertiserAccess
from report import get_auth_token
import json
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User as DjangoUser

appnexus_url = settings.__dict__.get(
    'APPNEXUS_URL', 'https://api.appnexus.com/')

user_types_can_write=frozenset(('member_advertiser','member',)) # 'bidder' ???

def load_appnexus_permissions(user):
    if not isinstance(user,(DjangoUser, FrameworkUser)):
        print 'load_appnexus_permissions expects Django user as parameter'
        return False
    if user is DjangoUser:
        user = user.frameworkuser
        if not user:
            return False
    if not user.apnexus_user_id:
        user.use_appnexus_rights = False
        user.appnexus_can_write = False;
        return False
    old_id = FrameworkUser.objects.get(pk=user.pk).apnexus_user_id
    if user.apnexus_user_id == old_id:
        return False

    user.appnexus_can_write = user.apnexus_user.user_type in user_types_can_write

    try:
        url = appnexus_url + User.api_endpoint
        token = get_auth_token()
        r = requests.get(
            url, params={'id':user.apnexus_user_id}, headers={
                "Authorization": token})
        response = json.loads(r.content)['response']
        user_data = response['user']
        rights=user_data["advertiser_access"] or [user_data['advertiser_id']]
        objs=map(lambda x:UserAdvertiserAccess(user_id=user.apnexus_user_id,advertiser_id=x),
                 filter(None, rights))
        UserAdvertiserAccess.objects.filter(user_id=user.apnexus_user_id).delete()
        UserAdvertiserAccess.objects.bulk_create(objs)

    except Exception as e:
        print 'In func "load_appnexus_permissions" raised error:',e

@receiver(pre_save, sender=FrameworkUser)
def framework_user_pre_save(sender, **kwargs):
    load_appnexus_permissions(kwargs.get('instance'))