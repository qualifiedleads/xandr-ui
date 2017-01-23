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
    now = datetime.datetime.now()
    params = parse_get_params(request.GET)
    from_date = params["from_date"]
    to_date = params["to_date"]
    advertiser_id = request.GET.get("advertiser_id")
    filt, order = getFilterQueryString(params["filter"], request.GET.get("sort"), request.GET.get("order"))
    queryRes = VideoAdCampaigns.objects.raw("""
select page.*,
  array((select
           json_build_object(
           'day', vac.date,
           'imp', coalesce(SUM(imp_hour),0),
           'spend', coalesce(SUM(spent_hour),0),
           'ad_starts', coalesce(SUM(ad_starts_hour),0),
           'fill_rate', coalesce(case SUM(imp_hour) when 0 then 0 else SUM(ad_starts_hour)::float/SUM(imp_hour) end,0),
           'profit_loss', coalesce(SUM(spent_cpvm_hour) - SUM(spent_hour), -SUM(spent_hour), SUM(spent_cpvm_hour),0))
         from video_ad_campaigns vac
         where vac.campaign_id=page.campaign_id
           AND date >='""" + str(from_date) + """' AND date <='""" + str(to_date) + """'
         group by vac.campaign_id, vac.date
         order by vac.date)) id
from (
      select distinct on (video_ad_campaigns.campaign_id)
        video_ad_campaigns.campaign_id,
        campaign.name,
        SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) imps,
        SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id) spent,
        case SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) when 0 then 0 else (SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id))/(SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id))*1000 end cpm,
        SUM(video_ad_campaigns.ad_starts_hour) over (partition by video_ad_campaigns.campaign_id) ad_starts,
        SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id) cpvm,
        case SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) when 0 then 0 else (SUM(video_ad_campaigns.ad_starts_hour) over (partition by video_ad_campaigns.campaign_id))::float/(SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id)) end fill_rate,
        coalesce((SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id)) - (SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id)), -(SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id)), (SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id)), 0) AS profit_loss,
        first_value(video_ad_campaigns.fill_rate_hour) over w as delta_fill_rate,
        first_value(video_ad_campaigns.profit_loss_hour) over w as delta_profit_loss
      FROM
        video_ad_campaigns
        LEFT JOIN campaign on campaign_id = campaign.id
      WHERE
        video_ad_campaigns.advertiser_id=""" + str(advertiser_id) + """
        AND date >='""" + str(from_date) + """' AND date <='""" + str(to_date) + """'
      WINDOW w as (partition by video_ad_campaigns.campaign_id order by hour desc)
     ) page """ + ' ' + filt + ' ' + order +""" LIMIT """ + str(params["take"]) + """ OFFSET """ + str(params["skip"]))
    answer = {}
    answer["campaigns"] = []

    for row in queryRes:
        answer["campaigns"].append({
            "campaign_id": row.campaign_id,
            "campaign_name": row.campaign.name,
            "fill_rate_hour": checkFloat(row.delta_fill_rate),
            "profit_loss_hour": checkFloat(row.delta_profit_loss),
            "spent": checkFloat(row.spent),
            "sum_imps": checkInt(row.imps),
            "cpm": checkFloat(row.cpm),
            "ad_starts": checkInt(row.ad_starts),
            "fill_rate": checkFloat(row.fill_rate),
            "profit_loss": checkFloat(row.profit_loss),
            "chart": row.id
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
  COUNT(page.campaign_id) id,
  SUM(page.imps) total_sum_imps,
  SUM(page.spent) total_spent,
  case SUM(page.imps) when 0 then 0 else SUM(page.spent)/SUM(page.imps) end total_cpm,
  SUM(page.ad_starts) total_ad_starts,
  case SUM(page.imps) when 0 then 0 else SUM(page.ad_starts)::float/SUM(page.imps)*100 end total_fill_rate,
  coalesce(SUM(page.cpvm) - SUM(page.spent), -SUM(page.spent), SUM(page.cpvm),0) total_profit_loss,
  SUM(delta_profit_loss) total_profit_loss_hour,
  case SUM(page.last_imp_hour) when 0 then 0 else SUM(page.last_ad_starts_hour)::float/SUM(page.last_imp_hour)*100 end total_fill_rate_hour
from (
      select distinct on (video_ad_campaigns.campaign_id)
        video_ad_campaigns.campaign_id,
        campaign.name,
        SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) imps,
        SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id) spent,
        case SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) when 0 then 0 else (SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id))/(SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id))*1000 end cpm,
        SUM(video_ad_campaigns.ad_starts_hour) over (partition by video_ad_campaigns.campaign_id) ad_starts,
        SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id) cpvm,
        case SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id) when 0 then 0 else (SUM(video_ad_campaigns.ad_starts_hour) over (partition by video_ad_campaigns.campaign_id))::float/(SUM(video_ad_campaigns.imp_hour) over (partition by video_ad_campaigns.campaign_id)) end fill_rate,
        coalesce((SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id)) - (SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id)), -(SUM(video_ad_campaigns.spent_hour) over (partition by video_ad_campaigns.campaign_id)), (SUM(video_ad_campaigns.spent_cpvm_hour) over (partition by video_ad_campaigns.campaign_id)), 0) AS profit_loss,
        first_value(video_ad_campaigns.imp_hour) over w as last_imp_hour,
        first_value(video_ad_campaigns.ad_starts_hour) over w as last_ad_starts_hour,
        first_value(video_ad_campaigns.fill_rate_hour) over w as delta_fill_rate,
        first_value(video_ad_campaigns.profit_loss_hour) over w as delta_profit_loss
      FROM
        video_ad_campaigns
        LEFT JOIN campaign on campaign_id = campaign.id
      WHERE
        video_ad_campaigns.advertiser_id=""" + str(advertiser_id) + """
        AND date >='""" + str(from_date) + """' AND date <='""" + str(to_date) + """'
      WINDOW w as (partition by video_ad_campaigns.campaign_id order by hour desc)
     ) page """ + str(filt))
    ans = list(queryRes)
    return ans[0]

def getFilterQueryString(incFilters, incSort, incOrder):#
    vocabulary = {}
    vocabulary["campaign"] = "page.name"
    vocabulary["spent"] = "page.spent"
    vocabulary["sum_imps"] = "page.imps"
    vocabulary["cpm"] = "page.cpm"
    vocabulary["ad_starts"] = "page.ad_starts"
    vocabulary["fill_rate"] = "page.fill_rate*100"
    vocabulary["profit_loss"] = "page.profit_loss"
    vocabulary["fill_rate_hour"] = "page.delta_fill_rate*100"
    vocabulary["profit_loss_hour"] = "page.delta_profit_loss"

    ansWhere = "WHERE ("
    ansOrder = "ORDER BY "

    if str(incSort) == "campaign":
        ansOrder = ansOrder + vocabulary[str(incSort)] + ' ' + str(incOrder)
    else:
        if str(incOrder) == "asc":
            order = "desc"
        else:
            order = "asc"
        ansOrder = ansOrder + '-' + vocabulary[str(incSort)] + ' ' + order
    equlitiesMarks = ["=", "<=", ">="]

    clause = re.compile(r'\s*\[\s*"([^"]*)",\s*"([^"]*)",\s*(\w+|\d+(?:\.\d*)?|(?:"(?:[^"]|\\\S)*"))\s*\]')
    separatedFilters = re.findall(clause, incFilters)
    #one condition
    if not separatedFilters:
        clause = re.compile(r"^(.*?)(>|<|=|<>|>=|<=|\bcontains\b|\bnotcontains\b|\bstartswith\b|\bendswith\b)(.*)$")
        separatedFilters = re.match(clause, incFilters)
        if separatedFilters is None:# without filtration
            return '', ansOrder
        else:
            filt = separatedFilters.string.split(' ')
            for i in xrange(3, len(filt)):# if campaign name have spaces
                filt[2] += (' ' + filt[i])
            if filt[0] == "campaign":
                if filt[1] == "<>":
                    return ansWhere + vocabulary[filt[0]] + " NOT LIKE '%%" + filt[2] + "%%')", ansOrder
                else:
                    return ansWhere + vocabulary[filt[0]] + " LIKE '%%" + filt[2] + "%%')", ansOrder
            else:
                if filt[1] in equlitiesMarks and filt[2] == '0':
                    filt[2] += (" OR " + vocabulary[filt[0]] + " IS NULL")
                if filt[1] == "<>":
                    if filt[2] == '0':
                        filt[2] += (" OR " + vocabulary[filt[0]] + " IS NOT NULL")
                    else:
                        filt[2] += (" OR " + vocabulary[filt[0]] + " IS NULL")

                return ansWhere + vocabulary[filt[0]] + filt[1] + filt[2] + ')', ansOrder
    #multiple conditions
    if separatedFilters[0][0] == "campaign":
        if separatedFilters[0][1] == "<>":
            ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + " NOT LIKE '%%" + separatedFilters[0][2][1:-1] + "%%'"
        else:
            ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + " LIKE '%%" + separatedFilters[0][2][
                                                                                     1:-1] + "%%'"
    else:
        temp = str(separatedFilters[0][2])
        if separatedFilters[0][1] in equlitiesMarks and separatedFilters[0][2] == '0':
            temp = temp + " OR " + str(vocabulary[separatedFilters[0][0]]) + " IS NULL"
        if separatedFilters[0][1] == "<>":
            if separatedFilters[0][2] == '0':
                temp += (" OR " + vocabulary[separatedFilters[0][0]] + " IS NOT NULL")
            else:
                temp += (" OR " + vocabulary[separatedFilters[0][0]] + " IS NULL")
        ansWhere = ansWhere + vocabulary[separatedFilters[0][0]] + separatedFilters[0][1] + temp
    lastColumn = separatedFilters[0][0]

    for i in xrange(1, len(separatedFilters)):
        if lastColumn == separatedFilters[i][0] and separatedFilters[i][1] == '=':# for between
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
            temp = str(separatedFilters[i][2])
            if separatedFilters[i][1] in equlitiesMarks and separatedFilters[i][2] == '0':
                temp = temp + " OR " + vocabulary[separatedFilters[i][0]] + " IS NULL"
            if separatedFilters[i][1] == "<>":
                if separatedFilters[i][2] == '0':
                    temp += (" AND " + vocabulary[separatedFilters[i][0]] + " IS NOT NULL")
                else:
                    temp += (" OR " + vocabulary[separatedFilters[i][0]] + " IS NULL")
            ansWhere = ansWhere + vocabulary[separatedFilters[i][0]] + separatedFilters[i][1] + temp
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

    queryRes = VideoAdCampaigns.objects.raw("""
SELECT
  date id,
  coalesce(SUM(imp_hour),0) sum_imp,
  coalesce(SUM(spent_hour),0) sum_spend,
  coalesce(SUM(ad_starts_hour),0) ad_starts,
  coalesce(case SUM(imp_hour) when 0 then 0 else SUM(ad_starts_hour)::float / SUM(imp_hour) end,0) fill_rate,
  coalesce(SUM(spent_cpvm_hour)-SUM(spent_hour), -SUM(spent_hour),SUM(spent_cpvm_hour),0) profit_loss
FROM
  video_ad_campaigns
WHERE
  advertiser_id=""" + str(advertiser_id) + """
  AND
  date >='""" + str(from_date) + """'
  AND
  date <='""" + str(to_date) + """'
GROUP BY
  date
ORDER BY
  date;
    """)

    answer = []
    for row in queryRes:
        answer.append({
            "day": row.id,
            "imp": row.sum_imp,
            "spend": row.sum_spend,
            "ad_starts": row.ad_starts,
            "fill_rate": row.fill_rate,
            "profit_loss": row.profit_loss
        })
    return Response(answer)

def checkFloat(number):
    return 0 if number is None else float(number)

def checkInt(number):
    return 0 if number is None else int(number)