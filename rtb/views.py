import itertools, time, datetime, re, decimal, filter_func
from urllib import addbase

from django.http import JsonResponse
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField
from django.db.models.functions import Coalesce
from models import SiteDomainPerformanceReport, Campaign, GeoAnaliticsReport
from django.core.cache import cache
from pytz import utc
import operator
from rest_framework.decorators import api_view, parser_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.authentication import TokenAuthentication
import ast
from utils import parse_get_params, make_sum, check_user_advertiser_permissions
from django.contrib.auth.decorators import login_required, user_passes_test
import countries
from rest_framework import status


def to_unix_timestamp(d):
    return str(int(time.mktime(d.timetuple())))


zero_sum = {
    'conv': 0,
    'cpc': 0,
    'cpm': 0,
    'cvr': 0,
    'ctr': 0,
    'spend': 0,
    # 'media_cost': 0,
    'conv_click': 0,
    # 'post_click_convs': 0,
    'conv_view': 0,
    # 'post_view_convs': 0,
    'imp': 0,
    # 'imps': 0,
    'clicks': 0,
    'imps_viewed': 0,
    'view_measured_imps': 0,
    'view_rate': 0,
    'view_measurement_rate': 0,

}


def calc_another_fields(obj):
    res = {
        'conv': None,
        'cpc': None,
        'cpm': None,
        'cvr': None,
        'ctr': None,
        # 'imps_viewed': None,
        # 'view_measured_imps': None,
        'view_rate': None,
        'view_measurement_rate': None,
    }
    res.update(obj)
    try:
        res['conv'] = (obj.get('conv', 0) or 0) + (obj.get('conv_click', 0) or 0) + (obj.get('conv_view', 0) or 0)
        res['cpc'] = float(obj['spend']) / obj['clicks'] if obj['clicks'] else 0
        res['cpm'] = float(obj["spend"]) / obj['imp'] * 1000 if obj['imp'] else 0
        res['cvr'] = float(res["conv"])* 100.0 / obj['imp'] if obj['imp'] else 0
        res['ctr'] = float(obj["clicks"])*100.0 / obj['imp'] if obj['imp'] else 0
        res['view_rate'] = 100.0 * float(obj['imps_viewed']) / obj['view_measured_imps'] if obj['view_measured_imps'] else 0
        res['view_measurement_rate'] = 100.0 * float(obj['view_measured_imps']) / obj['imp'] if obj['imp'] else 0
    except:
        pass
    res.pop('conv_click', None)
    res.pop('conv_view', None)
    res.pop('campaign', None)

    return res


def get_campaigns_data(advertiser_id, from_date, to_date):
    key = '_'.join(('rtb_campaigns', str(advertiser_id), from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    # calc campaigns data
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id=advertiser_id,
        day__gte=from_date,
        day__lte=to_date,
    ).values('campaign', 'day').annotate(
        # spend=Sum('booked_revenue'),
        spend=Sum('media_cost'),
        # conv=Sum('convs_per_mm'),
        conv_click=Sum('post_click_convs'),
        conv_view=Sum('post_view_convs'),
        # conv=Sum('post_click_convs') + Sum('post_view_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
        # cpc=Sum('media_cost')/Sum('clicks'), #Cost per click
        ###cpc=Avg('cost_ecpc'),
        # cpm=Sum('media_cost')/Sum('imps')*1000, #Cost per view
        # cvr=(Sum('post_click_convs') + Sum('post_view_convs'))/Sum('imps'),
        # ctr=Sum('clicks') / Sum('imps'),
        imps_viewed=Sum('imps_viewed'),
        view_measured_imps=Sum('view_measured_imps'),

    ).order_by('campaign', 'day')
    campaigns = []
    campaign_names = dict(Campaign.objects.all().values_list('id', 'name'))
    for camp, camp_data in itertools.groupby(q, lambda x: x['campaign']):
        current_campaign = {}
        current_campaign['id'] = camp
        current_campaign['chart'] = map(calc_another_fields, camp_data)
        summary = reduce(make_sum, current_campaign['chart'], zero_sum)
        summary = calc_another_fields(summary)
        current_campaign.update(summary)
        current_campaign['campaign'] = campaign_names[camp]
        current_campaign.pop('day', None)
        campaigns.append(current_campaign)
    cache.set(key, campaigns)
    return campaigns


@api_view()
@check_user_advertiser_permissions()
@parser_classes([FormParser, MultiPartParser])
def campaigns(request):
    """
Get campaigns data for given period

## Url format: /api/v1/campaigns?from={from_date}&to={to_date}&skip={skip}&take={take}&sort={sort}&order={order}&stat_by={stat_by}&filter={filter}


+ Parameters

    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    + skip (number, optional) - How much records need to skip (pagination)
        + Default: 0
    + take (number, optional) - How much records need to return (pagination)
        + Default: 20
    + sort (string, optional) - Field to sort by
        + Default: campaign
    + order (string, optional) - Order of sorting (ASC or DESC)
        + Default: desc
    + stat_by (string, optional) - statistic fields to select
        + Format: comma separated
        + Example: impressions,cpa,cpc
        + Full field list:campaign, spend, conv, imp, clicks, cpc, cpm, cvr, ctr,view_measured_imps, view_rate, view_measurement_rate

    + filter (string, optional) - filter data by several fields
        + Format: special filter language
        + Example: TODO

    """
    allCampaignsInfo = {}
    params = parse_get_params(request.GET)
    filt, order = getUsualFilterQueryString(params["filter"], request.GET.get("sort"), request.GET.get("order"))
    try:
        queryRes = Campaign.objects.raw("""
    select
      campaign.id as main_id,
      campaign.name,
      camp_info.*
    from
      campaign
      left join ui_usual_campaigns_grid_data_""" + str(request.GET.get("type")) +""" camp_info
      on campaign.id=camp_info.campaign_id
    where
      campaign.state <> 'inactive'
    and
      advertiser_id=""" + str(request.GET.get("advertiser_id")) +
                                       ' ' + filt +
                                        ' ' + order +" LIMIT " + str(params["take"]) + " OFFSET " + str(params["skip"]) + ';')
        allCampaignsInfo["campaigns"] = []
        allCampaignsInfo["totalCount"] = len(Campaign.objects.filter(advertiser_id=request.GET.get("advertiser_id")))
        for row in queryRes:
            allCampaignsInfo["campaigns"].append({
                "id": row.main_id,
                "campaign": row.name,
                "clicks": 0 if row.clicks is None else row.clicks,
                "conv": 0 if row.conversions is None else row.conversions,
                "cpc": 0 if row.cpc is None else row.cpc,
                "cpm": 0 if row.cpm is None else row.cpm,
                "ctr": 0 if row.ctr is None else row.ctr*100,
                "cvr": 0 if row.cvr is None else row.cvr,
                "view_measurement_rate": 0 if row.view_measurement_rate is None else row.view_measurement_rate*100,
                "imp": 0 if row.imps is None else row.imps,
                "imps_viewed": 0 if row.imps_viewed is None else row.imps_viewed,
                "spend": 0 if row.spent is None else row.spent,
                "view_measured_imps": 0 if row.view_measured_imps is None else row.view_measured_imps,
                "view_rate": 0 if row.view_rate is None else row.view_rate*100,
                "chart": row.day_chart
            })

        return Response(allCampaignsInfo)
    except Exception, e:
        print "Can not get data for " + str(request.GET.get("advertiser_id")) + " advertiser. Error: " + str(e)
        return Response(status=status.HTTP_404_NOT_FOUND)


def getUsualFilterQueryString(incFilters, incSort, incOrder):
    vocabulary = {}
    vocabulary["campaign"] = "campaign.name"
    vocabulary["spend"] = "camp_info.spent"
    vocabulary["conv"] = "camp_info.conversions"
    vocabulary["imp"] = "camp_info.imps"
    vocabulary["clicks"] = "camp_info.clicks"
    vocabulary["cpc"] = "camp_info.cpc"
    vocabulary["cpm"] = "camp_info.cpm"
    vocabulary["cvr"] = "camp_info.cvr"
    vocabulary["ctr"] = "camp_info.ctr*100"

    vocabulary["imps_viewed"] = "camp_info.imps_viewed"
    vocabulary["view_measured_imps"] = "camp_info.view_measured_imps"
    vocabulary["view_measurement_rate"] = "camp_info.view_measurement_rate*100"
    vocabulary["view_rate"] = "camp_info.view_rate*100"

    ansWhere = "AND ("
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
    # one condition
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
    # multiple conditions
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


def get_days_data(advertiser_id, from_date, to_date):
    key = '_'.join(('rtb_days', str(advertiser_id), from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    res = {}
    # no cache hit
    # calc day data
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id=advertiser_id,
        day__gte=from_date,
        day__lte=to_date,
    ).values('day').annotate(
        spend=Sum('media_cost'),
        conv_click=Sum('post_click_convs'),
        conv_view=Sum('post_view_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
        imps_viewed=Sum('imps_viewed'),
        view_measured_imps=Sum('view_measured_imps'),
    ).order_by('day')
    days = map(calc_another_fields, q)
    summary = reduce(make_sum, days, zero_sum)
    summary = calc_another_fields(summary)
    summary.pop('day', None)
    res['days'] = days
    res['totals'] = summary
    cache.set(key, res)
    return res


@api_view()
@check_user_advertiser_permissions()
def totals(request):
    """
## Totals [/api/v1/totals?from={from_date}&to={to_date}]

### get symmary data for given period [GET]

+ Parameters

    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274

    """
    params = parse_get_params(request.GET)
    data = get_days_data(params['advertiser_id'], params['from_date'], params['to_date'])
    return JsonResponse({"totals": data['totals']})


@api_view()
@check_user_advertiser_permissions()
def statistics(request):
    """
## Statistics [/api/v1/statistics?from={from_date}&to={to_date}&by={by}]

### Get total statistics [GET]

+ Parameters

    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    + by (string, optional) - statistic fields to select
        + Format: comma separated
        + Example: impressions,cpa,cpc
    """
    print 'Begin statistics'
    params = parse_get_params(request.GET)
    data = get_days_data(params['advertiser_id'], params['from_date'], params['to_date'])['days']
    print len(data)
    print params['stat_by']
    if params['stat_by'] and data:
        entries_to_remove = set(data[0]) - set(params['stat_by'])
        entries_to_remove.remove('day')
        print 'Fields to remove', entries_to_remove
        for camp in data:
            for f in entries_to_remove:
                camp.pop(f, None)
    return JsonResponse({'statistics': data})


@api_view()
@check_user_advertiser_permissions()
def map_clicks(request):
    """
## Map of clicks [/api/v1/map/clicks?from={from_date}&to={to_date}]

### Get count of clicks for each country [GET]

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
        Sum('clicks'),
    )
    d = dict(q)
    result_dict = {countries.CountryDict.get(k, k): d[k] for k in d}
    return JsonResponse(result_dict)
