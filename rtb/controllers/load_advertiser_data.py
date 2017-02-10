from rest_framework.decorators import api_view
from rest_framework.response import Response
from rtb.cron import load_only_one_advertiser_data
from rtb.report import get_auth_token

appnexusUrl = 'https://api.appnexus.com/'


@api_view(['GET'])
# @check_user_advertiser_permissions(campaign_id_num=0)
def loadAdvertiserData(request, id):
    """
GET

## Url format: /api/v1/advertiser/(\d+)/update

    advertiserId: id
    """
    try:
        if request.method == "GET":
            token = get_auth_token()
            status = load_only_one_advertiser_data(token, False, True, isLastModified=True, advId=id)
            return Response(status=status)
    except Exception, e:
        print 'Error: ' + str(e)
        return Response(status=500)

