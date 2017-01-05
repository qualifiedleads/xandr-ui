from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rtb.models import Advertiser, SiteDomainPerformanceReport, GeoAnaliticsReport
from rest_framework import status
from django.db.models import Sum
from django.http import JsonResponse
from rtb.utils import parse_get_params
import rtb.countries


@api_view(["PUT"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSetAdType(request):
    try:
        Advertiser.objects.filter(id=request.data.get("id")).update(ad_type=request.data.get("ad_type"))
    except Exception, e:
        print "Can not update advertiser type: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSendVideoCampaingData(request):
    advertiser_id = request.GET.get("advertiser_id")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSendMapImpsData(request):
    """
    ## Map of imps [/api/v1/map/imps?from={from_date}&to={to_date}]

    ### Get count of imps for each country [GET]

    + Parameters

        + from_date (date) - Date to select statistics from
            + Format: Unixtime
            + Example: 1466667274
        + to_date (date) - Date to select statistics to
            + Format: Unixtime
            + Example: 1466667274

        """
    params = parse_get_params(request.GET)
    q = GeoAnaliticsReport.objects.filter(
        advertiser_id=params['advertiser_id'],
        day__gte=params['from_date'],
        day__lte=params['to_date'],
    ).values_list('geo_country_name').annotate(
        Sum('imps'),
    )
    d = dict(q)
    result_dict = {rtb.countries.CountryDict.get(k, k): d[k] for k in d}
    return JsonResponse(result_dict)

@api_view(["GET"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSendVideoCampaingStatistics(request):
    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
# @check_user_advertiser_permissions(campaign_id_num=0)
def apiSendVideoCampaingTotals(request):
    return Response(status=status.HTTP_200_OK)