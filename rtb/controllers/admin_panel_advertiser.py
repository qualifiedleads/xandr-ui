from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rtb.models import Advertiser

@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetAdType(request):
    try:
        Advertiser.objects.filter(id=request.data.get("id")).update(ad_type=request.data.get("ad_type"))
    except Exception, e:
        print "Can not update advertiser type: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetToken(request):
    try:
        Advertiser.objects.filter(id=request.data.get("id")).update(token=request.data.get("token"))
    except Exception, e:
        print "Can not update advertiser token: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetAdDataSource(request):
    try:
        Advertiser.objects.filter(id=request.data.get("id")).update(grid_data_source=request.data.get("data_source"))
    except Exception, e:
        print "Can not update advertiser data source: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)

@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetAdRulesType(request):
    try:
        Advertiser.objects.filter(id=request.data.get("id")).update(rules_type=request.data.get("rules_type"))
    except Exception, e:
        print "Can not update advertiser rules type: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)