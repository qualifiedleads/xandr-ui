from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rtb.models import Advertiser, SiteDomainPerformanceReport, GeoAnaliticsReport
from rest_framework import status
from django.db.models import Sum
from django.http import JsonResponse
from rtb.utils import parse_get_params
import rtb.countries
from rtb.models.video_ad_models import VideoAdCampaigns
import re


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
def apiSendVideoCampaignData(request):
    params = parse_get_params(request.GET)
    from_date = params["from_date"]
    to_date = params["to_date"]
    advertiser_id = request.GET.get("advertiser_id")
    filt, order = getFilterQueryString(params["filter"], request.GET.get("sort"), request.GET.get("order"))
    print filt
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
              video.cpvm,
              CASE report.sum_imps WHEN 0 THEN 0 ELSE video.ad_starts::float/report.sum_imps*100 end fill_rate,
              coalesce(report.cpm * report.sum_imps - video.cpvm * video.ad_starts,report.cpm * report.sum_imps,-video.cpvm * video.ad_starts,0) AS profit_loss
            FROM
              campaign AS camp
              RIGHT JOIN(
                SELECT
                  campaign_id,
                  SUM(media_cost) AS sum_cost,
                  SUM(imps) AS sum_imps,
                  case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps) end cpm
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
                  SUM(cpvm) AS allcpvm,
                  case COUNT("CpId") when 0 then 0 else COUNT("CpId") end ad_starts,
                  case COUNT("CpId") when 0 then 0 else SUM(cpvm)/COUNT("CpId") end cpvm
                FROM
                  rtb_adstart_tracker
                WHERE
                  "AdvId" = """ + str(advertiser_id) + """
                  AND
                  "Date" >='""" + str(from_date) + """'
                  AND
                  "Date" <='""" + str(to_date) + """'
                GROUP BY
                  "CpId"
              ) AS video
              ON report.campaign_id=video."CpId"
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
            """+filt + ' ' + order + " LIMIT " + str(params["take"]) + " OFFSET " + str(params["skip"]))
    answer = {}
    answer["campaigns"] = []

    for row in queryRes:
        answer["campaigns"].append({
            "campaign_id": row.campaign_id,
            "campaign_name": row.name,
            "imp_hour": checkInt(row.imp_hour),
            "ad_starts_hour": checkInt(row.ad_starts_hour),
            "spent_hour": checkFloat(row.spent_hour),
            "cpm_hour": checkFloat(row.cpm_hour),
            "fill_rate_hour": checkFloat(row.fill_rate_hour)*100,
            "profit_loss_hour": checkFloat(row.profit_loss_hour),
            "cpvm_hour": checkFloat(row.cpvm_hour),
            "spent_cpvm_hour": checkFloat(row.spent_cpvm_hour),
            "spent": checkFloat(row.sum_cost),
            "sum_imps": checkInt(row.sum_imps),
            "cpm": checkFloat(row.cpm),
            "allcpvm": checkFloat(row.allcpvm),
            "ad_starts": checkInt(row.ad_starts),
            "cpvm": checkFloat(row.cpvm),

            "fill_rate": checkFloat(row.fill_rate),
            "profit_loss": checkFloat(row.profit_loss)
        })

    totals = getVideoCampaignSummary(request)#get totals
    answer["total_imp_hour"] = checkInt(totals.total_imp_hour)
    answer["total_ad_starts_hour"] = checkInt(totals.total_ad_starts_hour)
    answer["total_spent_hour"] = checkFloat(totals.total_spent_hour)
    answer["total_cpm_hour"] = checkFloat(totals.total_cpm_hour)
    answer["total_profit_loss_hour"] = checkFloat(totals.total_profit_loss_hour)
    answer["total_profit_loss"] = checkFloat(totals.total_profit_loss)
    answer["total_cpvm_hour"] = checkFloat(totals.total_cpvm_hour)
    answer["total_spent_cpvm_hour"] = checkFloat(totals.total_spent_cpvm_hour)
    answer["total_spent"] = checkFloat(totals.total_spent)
    answer["total_sum_imps"] = checkInt(totals.total_sum_imps)
    answer["total_cpm"] = checkFloat(totals.total_cpm)
    answer["total_allcpvm"] = checkFloat(totals.total_allcpvm)
    answer["total_ad_starts"] = checkInt(totals.total_ad_starts)
    answer["total_cpvm"] = checkFloat(totals.total_cpvm)

    answer["total_count"] = totals.total_count

    answer["total_fill_rate"] = checkFloat(totals.total_fill_rate)
    answer["total_fill_rate_hour"] = checkFloat(totals.total_fill_rate_hour)
    return Response(answer)

def getVideoCampaignSummary(request):
    params = parse_get_params(request.GET)
    from_date = params["from_date"]
    to_date = params["to_date"]
    advertiser_id = request.GET.get("advertiser_id")
    filt, order = getFilterQueryString(params["filter"], params["sort"], params["order"])
    queryRes = VideoAdCampaigns.objects.raw("""
                SELECT
                  count(report.sum_cost) AS total_count,
                  SUM(vac.imp_hour) AS total_imp_hour,
                  SUM(vac.ad_starts_hour) AS total_ad_starts_hour,
                  SUM(vac.spent_hour) AS total_spent_hour,
                  SUM(vac.cpm_hour) AS total_cpm_hour,
                  SUM(vac.fill_rate_hour) AS id,
                  SUM(vac.profit_loss_hour) AS total_profit_loss_hour,
                  SUM(vac.cpvm_hour) AS total_cpvm_hour,
                  SUM(vac.spent_cpvm_hour) AS total_spent_cpvm_hour,
                  SUM(report.sum_cost) AS total_spent,
                  SUM(report.sum_imps) AS total_sum_imps,
                  SUM(report.cpm) AS total_cpm,
                  SUM(video.allcpvm) AS total_allcpvm,
                  SUM(video.ad_starts) AS total_ad_starts,
                  SUM(video.cpvm) AS total_cpvm,
                  case SUM(report.sum_imps) when 0 then 0 else SUM(video.ad_starts)/SUM(report.sum_imps)*100 end total_fill_rate,
                  case SUM(vac.imp_hour) when 0 then 0 else SUM(vac.ad_starts_hour)/SUM(vac.imp_hour)*100 end total_fill_rate_hour,
                  case when sum(video.loss) is null then SUM(report.profit) else SUM(report.profit) - SUM(video.loss) end total_profit_loss
                FROM
                  campaign AS camp
                  RIGHT JOIN(
                    SELECT
                      campaign_id,
                      SUM(media_cost) AS sum_cost,
                      SUM(imps) AS sum_imps,
                      case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps) end cpm,
                      case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps) * SUM(imps) end profit
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
                      SUM(cpvm) AS allcpvm,
                      COUNT("CpId") ad_starts,
                      case COUNT("CpId") when 0 then 0 else SUM(cpvm)/COUNT("CpId") end cpvm,
                      case COUNT("CpId") when 0 then 0 else SUM(cpvm)/COUNT("CpId") * COUNT("CpId") end loss
                    FROM
                      rtb_adstart_tracker
                    WHERE
                      "AdvId" = """ + str(advertiser_id) + """
                      AND
                      "Date" >='""" + str(from_date) + """'
                      AND
                      "Date" <='""" + str(to_date) + """'
                    GROUP BY
                      "CpId"
                  ) AS video
                  ON report.campaign_id=video."CpId"
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
                """+str(filt))
    ans = list(queryRes)
    return ans[0]

def getFilterQueryString(incFilters, incSort, incOrder):#
    vocabulary = {}
    vocabulary["campaign"] = "camp.name"
    vocabulary["spent"] = "report.sum_cost"
    vocabulary["sum_imps"] = "report.sum_imps"
    vocabulary["cpm"] = "report.cpm"
    vocabulary["ad_starts"] = "video.ad_starts"

    vocabulary["fill_rate"] = "CASE report.sum_imps WHEN 0 THEN 0 ELSE video.ad_starts::float/report.sum_imps*100 end"
    vocabulary["profit_loss"] = "coalesce(report.cpm * report.sum_imps - video.cpvm * video.ad_starts,report.cpm * report.sum_imps,-video.cpvm * video.ad_starts,0)"

    vocabulary["fill_rate_hour"] = "vac.fill_rate_hour"
    vocabulary["profit_loss_hour"] = "vac.profit_loss_hour"

    ansWhere = "WHERE "
    ansOrder = "ORDER BY "

    ansOrder = ansOrder + vocabulary[str(incSort)] + ' ' + str(incOrder)

    clause = re.compile(r'\s*\[\s*"([^"]*)",\s*"([^"]*)",\s*(\w+|\d+(?:\.\d*)?|(?:"(?:[^"]|\\\S)*"))\s*\]')
    separatedFilters = re.findall(clause, incFilters)
    if not separatedFilters:
        clause = re.compile(r"^(.*?)(>|<|=|<>|>=|<=|\bcontains\b|\bnotcontains\b|\bstartswith\b|\bendswith\b)(.*)$")
        separatedFilters = re.match(clause, incFilters)
        if separatedFilters is None:
            return '', ansOrder
        else:
            filt = separatedFilters.string.split(' ')
            for i in xrange(3, len(filt)):
                filt[2] += (' ' + filt[i])
            if filt[0] == "campaign":
                return ansWhere + vocabulary[filt[0]] + " LIKE '" + filt[2] + "%%'", ansOrder
            else:
                return ansWhere + vocabulary[filt[0]] + filt[1] + filt[2], ansOrder
    for filt in separatedFilters:
        if filt[0] == "campaign":
            ansWhere = ansWhere + vocabulary[filt[0]] + " LIKE '" + filt[2] + "%%' AND "
        else:
            ansWhere = ansWhere + vocabulary[filt[0]] + filt[1] + filt[2] + " AND "
    if ansWhere == "WHERE ":
        return '', ansOrder
    return ansWhere[:-5], ansOrder

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
def apiSendVideoCampaignStatistics(request):
    params = parse_get_params(request.GET)
    from_date = params["from_date"]
    to_date = params["to_date"]
    advertiser_id = request.GET.get("advertiser_id")

    queryRes = SiteDomainPerformanceReport.objects.raw("""
            SELECT
              DISTINCT m_rep.day::timestamp::date AS id,
              report.sum_imp AS imp,
              report.sum_spend AS spend,
              video.ad_s AS ad_starts,
              case report.sum_imp when 0 then 0 else video.ad_s::float / report.sum_imp end fill_rate,
              report.cpm * report.sum_imp - video.cpvm * video.ad_s AS profit_loss
            FROM
              site_domain_performance_report m_rep
              LEFT JOIN(
                SELECT
                  "Date"::timestamp::date AS dates,
                  COUNT("AdvId") AS ad_s,
                  case COUNT("AdvId") when 0 then 0 else SUM(cpvm)/COUNT("AdvId") end cpvm
                FROM
                  rtb_adstart_tracker
                WHERE
                  "AdvId"=""" + str(advertiser_id) + """
                AND
                  "Date" >= '""" + str(from_date) + """'
                AND
                  "Date" <= '""" + str(to_date) + """'
                GROUP BY
                  "Date"::timestamp::date
              ) AS video
              ON m_rep.day=video.dates
              INNER JOIN(
                SELECT
                  day::timestamp::date AS sum_date,
                  SUM(imps) AS sum_imp,
                  SUM(media_cost) AS sum_spend,
                  case SUM(imps) when 0 then 0 else SUM(media_cost)::float/SUM(imps) end cpm
                FROM
                  site_domain_performance_report
                WHERE
                  advertiser_id = """ + str(advertiser_id) + """
                AND
                  day >= '""" + str(from_date) + """'
                AND
                  day <= '""" + str(to_date) + """'
                GROUP BY
                  day::timestamp::date
              ) AS report
              ON m_rep.day=report.sum_date
            WHERE
              day >= '""" + str(from_date) + """'
            AND
              day <= '""" + str(to_date) + """'
            ORDER BY
              m_rep.day::timestamp::date
            """)

    answer = []
    for row in queryRes:
        answer.append({
            "day": row.id,
            "imp": row.imp,
            "spend": row.spend,
            "ad_starts": row.ad_starts,
            "fill_rate": row.fill_rate,
            "profit_loss": row.profit_loss
        })
    return Response(answer)

def checkFloat(number):
    return 0 if number is None else float(number)

def checkInt(number):
    return 0 if number is None else int(number)