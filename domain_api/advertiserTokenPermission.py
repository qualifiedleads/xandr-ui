from rest_framework.permissions import BasePermission
from rtb.models import Advertiser


class AdvertiserTokenPermission(BasePermission):

    def has_permission(self, request, view):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            advertiser = list(Advertiser.objects.filter(token=token))
            if len(advertiser) != 0:
                return True
            return False
        except Exception as e:
            return False