from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rtb.models import Advertiser, SiteDomainPerformanceReport, GeoAnaliticsReport
from rest_framework import status
from django.db.models import Sum
from django.http import JsonResponse
from rtb.utils import parse_get_params
import rtb.countries
from rtb.models.video_ad_models import VideoAdCampaigns


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
    params = parse_get_params(request.GET)
    from_date = params["from_date"]
    to_date = params["to_date"]
    advertiser_id = request.GET.get("advertiser_id")
    queryRes = VideoAdCampaigns.objects.raw("""
            SELECT
              vac.id,
              camp.id AS campaign_id,
              camp.name,
              vac.imp_hour,
              vac.ad_starts_hour,
              vac.spent_hour,
              vac.cpm_hour,
              vac.fill_rate_hour,
              vac.profit_loss_hour,
              vac.cpvm_hour,
              vac.spent_cpvm_hour,
              report.sum_cost,
              report.sum_imps,
              report.cpm,
              video.allcpvm,
              video.ad_starts,
              video.cpvm
            FROM
              campaign AS camp
              RIGHT JOIN(
                SELECT
                  campaign_id,
                  SUM(media_cost) AS sum_cost,
                  SUM(imps) AS sum_imps,
                  case SUM(imps) when 0 then 0 else SUM(media_cost)::float/SUM(imps) end cpm
                FROM
                  site_domain_performance_report
                WHERE
                  day >= '""" + str(from_date) + """'
                  AND
                  day <= '""" + str(to_date) + """'
                  AND
                  advertiser_id = """ + str(advertiser_id) + """
                GROUP BY
                  campaign_id
              ) AS report
              ON report.campaign_id=camp.id
              LEFT JOIN(
                SELECT
                  "CpId",
                  SUM(cpvm::float) AS allcpvm,
                  case COUNT("CpId") when 0 then 0 else COUNT("CpId") end ad_starts,
                  case COUNT(id) when 0 then 0 else SUM(cpvm::float)/COUNT("CpId") end cpvm
                FROM
                  rtb_adstart_tracker
                WHERE
                  "AdvId" = '""" + str(advertiser_id) + """'
                  AND
                  "Date" >='""" + str(from_date) + """'
                  AND
                  "Date" <='""" + str(to_date) + """'
                GROUP BY
                  "CpId"
              ) AS video
              ON report.campaign_id=video."CpId"::integer
              LEFT JOIN(
                SELECT
                  id,
                  campaign_id,
                  imp_hour,
                  ad_starts_hour,
                  spent_hour,
                  cpm_hour,
                  fill_rate_hour,
                  profit_loss_hour,
                  cpvm_hour,
                  spent_cpvm_hour
                FROM
                  video_ad_campaigns v
                INNER JOIN(
                  SELECT
                    MAX(date) max_date
                  FROM
                    video_ad_campaigns
                  WHERE
                    advertiser_id=""" + str(advertiser_id) + """
                ) AS max_vac_date
                ON max_vac_date.max_date=v.date
              ) AS vac
              ON report.campaign_id=vac.campaign_id
            """)

    answer = {}
    answer["campaigns"] = []
    answer["total_imp_hour"] = 0
    answer["total_ad_starts_hour"] = 0
    answer["total_spent_hour"] = 0
    answer["total_cpm_hour"] = 0
    answer["total_profit_loss_hour"] = 0
    answer["total_profit_loss"] = 0
    answer["total_cpvm_hour"] = 0
    answer["total_spent_cpvm_hour"] = 0
    answer["total_spent"] = 0
    answer["total_sum_imps"] = 0
    answer["total_cpm"] = 0
    answer["total_allcpvm"] = 0
    answer["total_ad_starts"] = 0
    answer["total_cpvm"] = 0

    for row in queryRes:
        answer["campaigns"].append({
            "campaign_id": row.campaign_id,
            "campaign_name": row.name,
            "imp_hour": row.imp_hour,
            "ad_starts_hour": row.ad_starts_hour,
            "spent_hour": row.spent_hour,
            "cpm_hour": row.cpm_hour,
            "fill_rate_hour": row.fill_rate_hour,
            "profit_loss_hour": row.profit_loss_hour,
            "cpvm_hour": row.cpvm_hour,
            "spent_cpvm_hour": row.spent_cpvm_hour,
            "spent": row.sum_cost,
            "sum_imps": row.sum_imps,
            "cpm": row.cpm,
            "allcpvm": row.allcpvm,
            "ad_starts": row.ad_starts,
            "cpvm": row.cpvm
        })

        for key, value in answer["campaigns"][-1].iteritems():
            if value is None:
                answer["campaigns"][-1][key] = 0
        if answer["campaigns"][-1]["sum_imps"] == 0:
            answer["campaigns"][-1]["fill_rate"] = 0
        else:
            answer["campaigns"][-1]["fill_rate"] = float(answer["campaigns"][-1]["ad_starts"]) / \
                                                   answer["campaigns"][-1]["sum_imps"]
        answer["campaigns"][-1]["profit_loss"] = answer["campaigns"][-1]["cpm"] * answer["campaigns"][-1][
            "sum_imps"] - answer["campaigns"][-1]["cpvm"] * answer["campaigns"][-1]["ad_starts"]

        answer["total_imp_hour"] += int(answer["campaigns"][-1]["imp_hour"])
        answer["total_ad_starts_hour"] += int(answer["campaigns"][-1]["ad_starts_hour"])
        answer["total_spent_hour"] += float(answer["campaigns"][-1]["spent_hour"])
        answer["total_cpm_hour"] += float(answer["campaigns"][-1]["cpm_hour"])
        answer["total_profit_loss_hour"] += float(answer["campaigns"][-1]["profit_loss_hour"])
        answer["total_cpvm_hour"] += float(answer["campaigns"][-1]["cpvm_hour"])
        answer["total_spent_cpvm_hour"] += float(answer["campaigns"][-1]["spent_cpvm_hour"])
        answer["total_spent"] += float(answer["campaigns"][-1]["spent"])
        answer["total_sum_imps"] += int(answer["campaigns"][-1]["sum_imps"])
        answer["total_cpm"] += float(answer["campaigns"][-1]["cpm"])
        answer["total_allcpvm"] += float(answer["campaigns"][-1]["allcpvm"])
        answer["total_ad_starts"] += int(answer["campaigns"][-1]["ad_starts"])
        answer["total_cpvm"] += float(answer["campaigns"][-1]["cpvm"])
        answer["total_profit_loss"] += answer["campaigns"][-1]["profit_loss"]
    if answer["total_sum_imps"] == 0:
        answer["total_fill_rate"] = 0
    else:
        answer["total_fill_rate"] = float(answer["total_ad_starts"]) / answer["total_sum_imps"]
    if answer["total_imp_hour"] == 0:
        answer["total_fill_rate_hour"] = 0
    else:
        answer["total_fill_rate_hour"] = float(answer["total_ad_starts_hour"]) / answer["total_imp_hour"]
    answer["total_count"] = len(answer["campaigns"])
    return Response(answer)

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