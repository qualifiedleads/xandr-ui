from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rtb.models import Advertiser, SiteDomainPerformanceReport, GeoAnaliticsReport, RtbAdStartTracker
from rest_framework import status
from django.db.models import Sum
from django.http import JsonResponse
from rtb.utils import parse_get_params
import rtb.countries
from rtb.models.video_ad_models import VideoAdCampaigns
import re
import collections
import datetime


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
    queryRes = VideoAdCampaigns.objects.raw("""
            select
  video_ad_campaigns.campaign_id as id,
  video_ad_campaigns.campaign_name,
  report.spent,
  report.sum_imps,
  report.cpm,
  sum_data.ad_starts,
  case report.sum_imps when 0 then 0 else sum_data.ad_starts::float/report.sum_imps end fill_rate,
  coalesce(sum_data.spent_cpvm-report.spent,-report.spent,sum_data.spent_cpvm,0) AS profit_loss,
  video_ad_campaigns.fill_rate_hour,
  video_ad_campaigns.profit_loss_hour,
  stats
FROM
  video_ad_campaigns
  full JOIN (
    SELECT
      campaign_id,
      SUM(video_ad_campaigns.ad_starts_hour) ad_starts,
      SUM(video_ad_campaigns.spent_cpvm_hour) spent_cpvm,
      array((select
           json_build_object(
           'day', coalesce(vac.date, report.day),
           'imp', SUM(report.imps),
           'spend', SUM(report.media_cost),
           'ad_starts', SUM(ad_starts_hour),
           'fill_rate', case SUM(report.imps) when 0 then 0 else SUM(ad_starts_hour)::float/SUM(report.imps)*100 end,
           'profit_loss', coalesce(SUM(spent_cpvm_hour)-SUM(report.media_cost), -SUM(report.media_cost), SUM(spent_cpvm_hour), 0))
         from video_ad_campaigns as vac
           full JOIN (
             select
               campaign_id,
               day,
               imps,
               media_cost
             from site_domain_performance_report
             where advertiser_id=""" + str(advertiser_id) + """
              AND
                day >='""" + str(from_date) + """'
              AND
                day <='""" + str(to_date) + """'
             ) AS report
           ON report.campaign_id=vac.campaign_id
         where
           vac.campaign_id=video_ad_campaigns.campaign_id
         AND
           coalesce(vac.date, report.day) >='""" + str(from_date) + """'
         AND
           coalesce(vac.date, report.day) <='""" + str(to_date) + """'
         group by vac.campaign_id,coalesce(vac.date, report.day))) stats
    FROM
      video_ad_campaigns
    WHERE
      advertiser_id=""" + str(advertiser_id) + """
    AND
      date >='""" + str(from_date) + """'
    AND
      date <='""" + str(to_date) + """'
    GROUP BY
      campaign_id
    ) AS sum_data
    ON video_ad_campaigns.campaign_id = sum_data.campaign_id
  FULL OUTER JOIN(
    SELECT
      campaign_id,
      SUM(media_cost) AS spent,
      SUM(imps) AS sum_imps,
      case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps)*1000 end cpm
    FROM
      site_domain_performance_report
    WHERE
      advertiser_id=""" + str(advertiser_id) + """
    AND
      day >='""" + str(from_date) + """'
    AND
      day <='""" + str(to_date) + """'
    GROUP BY
      campaign_id
    ) AS report
    ON video_ad_campaigns.campaign_id = report.campaign_id
WHERE
  advertiser_id=""" + str(advertiser_id) + """
  and video_ad_campaigns.hour = (
      SELECT
        MAX(hour) max_date
      FROM
        video_ad_campaigns
      WHERE
        advertiser_id=""" + str(advertiser_id) + """
    )"""+filt + ' ' + order + " LIMIT " + str(params["take"]) + " OFFSET " + str(params["skip"]))
    answer = {}
    answer["campaigns"] = []

    for row in queryRes:
        answer["campaigns"].append({
            "campaign_id": row.id,
            "campaign_name": row.campaign_name,
            "fill_rate_hour": checkFloat(row.fill_rate_hour),
            "profit_loss_hour": checkFloat(row.profit_loss_hour),
            "spent": checkFloat(row.spent),
            "sum_imps": checkInt(row.sum_imps),
            "cpm": checkFloat(row.cpm),
            "ad_starts": checkInt(row.ad_starts),
            "fill_rate": checkFloat(row.fill_rate),
            "profit_loss": checkFloat(row.profit_loss),
            "chart": row.stats
        })

    totals = getVideoCampaignSummary(request)#get totals
    answer["total_profit_loss_hour"] = checkFloat(totals.total_profit_loss_hour)
    answer["total_profit_loss"] = checkFloat(totals.total_profit_loss)
    answer["total_spent"] = checkFloat(totals.total_spent)
    answer["total_sum_imps"] = checkInt(totals.total_sum_imps)
    answer["total_cpm"] = checkFloat(totals.total_cpm)
    answer["total_ad_starts"] = checkInt(totals.total_ad_starts)

    answer["total_count"] = totals.id

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
                select
  COUNT(video_ad_campaigns.profit_loss_hour) id,
  SUM(report.spent) total_spent,
  SUM(report.sum_imps) total_sum_imps,
  case SUM(report.sum_imps) when 0 then 0 else SUM(report.spent)/SUM(report.sum_imps)*1000 end total_cpm,
  SUM(sum_data.ad_starts) total_ad_starts,
  case SUM(report.sum_imps) when 0 then 0 else SUM(sum_data.ad_starts)::float/SUM(report.sum_imps)*100 end total_fill_rate,
  SUM(coalesce(sum_data.spent_cpvm-report.spent,-report.spent,sum_data.spent_cpvm,0)) AS total_profit_loss,
  case SUM(video_ad_campaigns.imp_hour) when 0 then 0 else SUM(video_ad_campaigns.ad_starts_hour)::float/SUM(video_ad_campaigns.imp_hour)*100 end total_fill_rate_hour,
  SUM(video_ad_campaigns.profit_loss_hour) as total_profit_loss_hour
FROM
  video_ad_campaigns
  full JOIN (
    SELECT
      campaign_id,
      SUM(video_ad_campaigns.ad_starts_hour) ad_starts,
      SUM(video_ad_campaigns.spent_cpvm_hour) spent_cpvm
    FROM
      video_ad_campaigns
    WHERE
      advertiser_id=""" + str(advertiser_id) + """
    AND
      date >='""" + str(from_date) + """'
    AND
      date <='""" + str(to_date) + """'
    GROUP BY campaign_id
    ) AS sum_data
    ON video_ad_campaigns.campaign_id = sum_data.campaign_id
  FULL OUTER JOIN(
    SELECT
      campaign_id,
      SUM(media_cost) AS spent,
      SUM(imps) AS sum_imps,
      case SUM(imps) when 0 then 0 else SUM(media_cost)/SUM(imps)*1000 end cpm
    FROM
      site_domain_performance_report
    WHERE
      advertiser_id=""" + str(advertiser_id) + """
    AND
      day >='""" + str(from_date) + """'
    AND
      day <='""" + str(to_date) + """'
    GROUP BY campaign_id
    ) AS report
    ON video_ad_campaigns.campaign_id = report.campaign_id
WHERE
  advertiser_id=""" + str(advertiser_id) + """
  and video_ad_campaigns.hour = (
      SELECT
        MAX(hour) max_date
      FROM
        video_ad_campaigns
      WHERE
        advertiser_id=""" + str(advertiser_id) + """
    )"""+str(filt))
    ans = list(queryRes)
    return ans[0]

def getFilterQueryString(incFilters, incSort, incOrder):#
    vocabulary = {}
    vocabulary["campaign"] = "video_ad_campaigns.campaign_name"
    vocabulary["spent"] = "report.spent"
    vocabulary["sum_imps"] = "report.sum_imps"
    vocabulary["cpm"] = "report.cpm"
    vocabulary["ad_starts"] = "sum_data.ad_starts"
    vocabulary["fill_rate"] = "CASE report.sum_imps WHEN 0 THEN 0 ELSE sum_data.ad_starts::float/report.sum_imps*100 end"
    vocabulary["profit_loss"] = "coalesce(sum_data.spent_cpvm - report.spent, -report.spent, sum_data.spent_cpvm, 0)"
    vocabulary["fill_rate_hour"] = "video_ad_campaigns.fill_rate_hour*100"
    vocabulary["profit_loss_hour"] = "video_ad_campaigns.profit_loss_hour"

    ansWhere = " AND("
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
                if filt[1] == "<>":
                    return ansWhere + vocabulary[filt[0]] + " NOT LIKE '%%" + filt[2] + "%%')", ansOrder
                else:
                    return ansWhere + vocabulary[filt[0]] + " LIKE '%%" + filt[2] + "%%')", ansOrder
            else:
                return ansWhere + vocabulary[filt[0]] + filt[1] + filt[2] + ')', ansOrder
    if separatedFilters[0][0] == "campaign":
        if separatedFilters[0][1] == "<>":
            ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + " NOT LIKE '%%" + separatedFilters[0][2][1:-1] + "%%'"
        else:
            ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + " LIKE '%%" + separatedFilters[0][2][
                                                                                     1:-1] + "%%'"
    else:
        ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + separatedFilters[0][1] + separatedFilters[0][2]
    lastColumn = separatedFilters[0][0]

    for i in xrange(1, len(separatedFilters)):
        if lastColumn == separatedFilters[i][0] and separatedFilters[i][1] == '=':
            ansWhere += " OR "
        else:
            ansWhere += ") AND ("
        if separatedFilters[i][0] == "campaign":
            if separatedFilters[i][1] == "<>":
                ansWhere = ansWhere + vocabulary[separatedFilters[i][0]] + " NOT LIKE '%%" + separatedFilters[i][2][1:-1] + "%%'"
            else:
                ansWhere = ansWhere + vocabulary[separatedFilters[i][0]] + " LIKE '%%" + separatedFilters[i][2][
                                                                                         1:-1] + "%%'"
        else:
            ansWhere = ansWhere + vocabulary[separatedFilters[i][0]] + separatedFilters[i][1] + separatedFilters[i][2]
        lastColumn = separatedFilters[i][0]
    ansWhere += ')'

    return ansWhere, ansOrder

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
      day::timestamp::date AS id,
      SUM(imps) AS sum_imp,
      SUM(media_cost) AS sum_spend,
      case SUM(imps) when 0 then 0 else SUM(media_cost)::float/SUM(imps)*1000 end cpm
    FROM
      site_domain_performance_report
    WHERE
      advertiser_id = """ + str(advertiser_id) + """
    AND
      day >= '""" + str(from_date) + """'
    AND
      day <= '""" + str(to_date) + """'
    GROUP BY
      day
    """)
    dictAns = {}
    allCpms = {}
    for row in queryRes:
        dictAns[row.id] = {
            "day": row.id,
            "imp": checkInt(row.sum_imp),
            "spend": checkFloat(row.sum_spend),
            "ad_starts": 0,
            "fill_rate": 0,
            "profit_loss": (-checkFloat(row.sum_spend)/checkInt(row.sum_imp)*1000 * checkInt(row.sum_imp))
        }
        allCpms[row.id] = checkFloat(row.cpm)

    queryRes = RtbAdStartTracker.objects.raw("""
    SELECT
      date AS id,
      SUM(video_ad_campaigns.ad_starts_hour) ad_starts,
      SUM(video_ad_campaigns.cpvm_hour) cpvm
    FROM
      video_ad_campaigns
    WHERE
      advertiser_id=""" + str(advertiser_id) + """
    AND
      date >='""" + str(from_date) + """'
    AND
      date <='""" + str(to_date) + """'
    GROUP BY date;
    """)
    for row in queryRes:
        if row.id in dictAns:
            dictAns[row.id]["ad_starts"] = checkInt(row.ad_starts)
            dictAns[row.id]["fill_rate"] = 0 if dictAns[row.id]["imp"] == 0 else (float(dictAns[row.id]["ad_starts"]) / dictAns[row.id]["imp"] * 100)
            dictAns[row.id]["profit_loss"] = allCpms[row.id] * dictAns[row.id]["imp"] - float(row.cpvm) * row.ad_starts
        else:
            dictAns[row.id] = {
                "day": row.id,
                "imp": 0,
                "spend": 0,
                "ad_starts": checkInt(row.ad_starts),
                "fill_rate": 0,
                "profit_loss": (checkFloat(row.cpvm) * checkInt(row.ad_starts))
            }
    answer = []
    orderedAns = collections.OrderedDict(sorted(dictAns.items()))
    for key, value in orderedAns.iteritems():
        answer.append(value)
    return Response(answer)

def checkFloat(number):
    return 0 if number is None else float(number)

def checkInt(number):
    return 0 if number is None else int(number)