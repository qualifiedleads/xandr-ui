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
    if not isinstance(user, FrameworkUser):
        user = user.frameworkuser
        if not user:
            return False
    if not user.apnexus_user_id:
        user.use_appnexus_rights = False
        user.appnexus_can_write = False;
        return False
    # if not user.use_appnexus_rights:
    #     return False
    try:
        old_id = FrameworkUser.objects.get(pk=user.pk).apnexus_user_id
        if user.apnexus_user_id == old_id:
            return False
    except:
        pass
    user.appnexus_can_write = user.apnexus_user.user_type in user_types_can_write
    try:
        url = appnexus_url + User.api_endpoint
        token = get_auth_token()
        r = requests.get(
            url, params={'id':user.apnexus_user_id}, headers={
                "Authorization": token})
        response = json.loads(r.content)['response']
        user_data = response['user']
        rights=[x['id'] for x in (user_data.get("advertiser_access") or [])] \
               or [user_data['advertiser_id']]
        objs=[UserAdvertiserAccess(user_id=user.apnexus_user_id,advertiser_id=x) for x in rights if x]
        UserAdvertiserAccess.objects.filter(user_id=user.apnexus_user_id).delete()
        UserAdvertiserAccess.objects.bulk_create(objs)

    except Exception as e:
        print 'In func "load_appnexus_permissions" raised error:',e

@receiver(pre_save, sender=FrameworkUser)
def framework_user_pre_save(sender, **kwargs):
    load_appnexus_permissions(kwargs.get('instance'))