from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.http import JsonResponse
from utils import parse_get_params, make_sum, check_user_advertiser_permissions
from models import SiteDomainPerformanceReport, Campaign, GeoAnaliticsReport, NetworkAnalyticsReport_ByPlacement, \
    Placement, NetworkCarrierReport_Simple, NetworkDeviceReport_Simple
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField
from django.db.models.functions import Coalesce, Concat, ExtractWeekDay
from django.db import connection
from django.core.cache import cache
import itertools
import datetime
from pytz import utc
import filter_func
from models.ml_kmeans_model import MLPlacementDailyFeatures, MLClustersCentroidsKmeans, MLPlacementsClustersKmeans, \
MLExpertsPlacementsMarks, MLViewFullPlacementsData, MLTestDataSet
from rtb.ml_learn_kmeans import mlGetPlacementInfoKmeans, mlGetGoodClusters, mlGetTestNumber
from models.placement_state import PlacementState, CampaignRules
from rtb.placement_state import PlacementState as PlacementStateClass
from rest_framework import status
from models.rtb_impression_tracker import RtbImpressionTrackerPlacement, RtbImpressionTrackerPlacementDomain
from django.db import connection
from django.utils import timezone

import bisect
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from ml_auc import mlCalcAuc

@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def singleCampaign(request, id):
    """
Get campaign name by id

## Url format: /api/v1/campaigns/id

+ Parameters

    + id(Number) - id for getting information about company

    """
    obj = Campaign.objects.get(pk=id)
    return Response({'id': obj.id, 'campaign': obj.name})


zero_sum = {
    "clicks": 0,
    "mediaspent": 0,
    "conversions": 0,
    "impression": 0,
}


# cpa, cpc,  ctr, #clicks, mediaspent, conversions,impression
def calc_another_fields(obj):
    res = {
        "day": obj["day"],
        "cpa": None, "cpc": None, "ctr": None,
        "clicks": obj["clicks"],
        "mediaspent": obj["mediaspent"],
        "impression": obj["impression"],
        "imps_viewed": obj.get("imps_viewed"),
        "view_measured_imps": obj.get("view_measured_imps"),
        'view_rate': None, 'view_measurement_rate': None,
    }
    try:
        post_click_convs = obj['post_click_convs'] or 0
        post_view_convs = obj['post_view_convs'] or 0
        res['conversions'] = post_click_convs + post_view_convs
        res['cpc'] = float(obj['mediaspent']) / obj['clicks'] if obj['clicks'] else 0
        res['cpa'] = float(obj["mediaspent"]) / res['conversions'] if res['conversions'] else 0
        res['ctr'] = float(obj["clicks"])*100.0 / obj['impression'] if obj['impression'] else 0
        res['view_rate'] = 100.0 * float(obj['imps_viewed']) / float(obj['view_measured_imps']) if obj['view_measured_imps'] else 0
        res['view_measurement_rate'] = 100.0 * float(obj['view_measured_imps']) / float(obj['imp']) if obj['imp'] else 0

    except:
        pass
    return res


def get_campaign_data( campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res:
        print 'Read graphInfo from cache'
        return res
    print 'From ', from_date, 'to', to_date
    # no cache hit
    q = SiteDomainPerformanceReport.objects.filter(
        campaign_id=campaign_id,
        day__gte=from_date,
        day__lte=to_date,
    ).values('day').annotate(  # impression, cpa, cpc, clicks, mediaspent, conversions, ctr
        mediaspent=Sum('media_cost'),
        # conversions = Sum('post_click_convs')+Sum('post_view_convs'), # Do not control nulls
        post_click_convs=Sum('post_click_convs'),
        post_view_convs=Sum('post_view_convs'),
        clicks=Sum('clicks'),
        impression=Sum('imps'),
        imps_viewed=Sum('imps_viewed'),
        view_measured_imps=Sum('view_measured_imps'),
    ).order_by('day')
    print q.query
    res = map(calc_another_fields, q)
    cache.set(key, res)
    return res


@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def graphInfo(request, id):
    """
Get single campaign statistics data for given period by selected categories: impression, cpa, cpc, clicks, mediaspent, conversions, ctr

## Url format: /api/v1/campaigns/:id/graphinfo/?from_date={from_date}&to_date={to_date}

+ Parameters
    + id (Number) - id for getting information about company
    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    + by (string, optional) - statistic fields to select (select every field if param is empty)
        + Format: comma separated
        + Example: impressions,cpa,cpc

    """
    c = Campaign.objects.get(pk=int(id))
    if not c:
        return Response({'error': "Unknown object id %d" % id})
    #advertiser_id = c.advertiser_id
    params = parse_get_params(request.GET, ["impression", "cpa", "cpc", "clicks", "mediaspent", "conversions", "ctr",
                                            'imps_viewed', 'view_measured_imps', 'view_rate', 'view_measurement_rate',])
    res = get_campaign_data(id, params['from_date'], params['to_date'])
    return Response(res)


def get_campaign_cpa(advertiser_id, campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign_candle', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    # from_date -= datetime.timedelta(days=1)
    # from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, 23, tzinfo = utc)
    from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, tzinfo=utc)
    to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, tzinfo=utc)
    query = """
SELECT
  EXTRACT('dow' FROM "hour") AS "date",
  MIN("cpa") AS "low",
  MAX("cpa") AS "high",
  percentile_cont(0.25) WITHIN GROUP (ORDER BY "cpa") AS "open",
  percentile_cont(0.75) WITHIN GROUP (ORDER BY "cpa") AS "close",
  AVG("cpa") AS "avg"
FROM (SELECT
  "hour",
  SUM("total_convs") AS "convs",
  SUM("cost") AS "cost",
  CASE WHEN SUM("total_convs") <> 0 THEN SUM("cost")/SUM("total_convs") END AS "cpa"
FROM "network_analytics_report_by_placement"
WHERE ("hour" >= %(from_date)s
  AND "hour" <=  %(to_date)s
  AND "campaign_id" = %(campaign_id)s)
GROUP BY "hour") subquery
GROUP BY "date"
ORDER BY "date"
    """
    cursor = connection.cursor()
    cursor.execute(query, locals())
    res = [dict(zip(("date","low","high","open","close","avg"),x)) for x in cursor.fetchall()]
    cache.set(key, res)
    return res


@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def cpaReport(request, id):
    """
Get single campaign cpa report for given period to create boxplots

## Url format: /api/v1/campaigns/:id/cpareport?from_date={from_date}&to_date={to_date}

+ Parameters
    + id (Number) - id for getting information about company
    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274


    """
    c = Campaign.objects.get(pk=int(id))
    if not c:
        return Response({'error': "Unknown object id %d" % id})
    advertiser_id = c.advertiser_id
    params = parse_get_params(request.GET)
    from_date = params['from_date']
    to_date = params['to_date']
    # expand to week boundary
    d = from_date.weekday()
    if d>0:
        from_date -= datetime.timedelta(days=d)
    d = to_date.weekday()
    if d<6:
        to_date += datetime.timedelta(days=6-d)

    res = get_campaign_cpa(advertiser_id, id, from_date, to_date)
    return Response(res)


def get_campaign_placement(campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign_placement', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    wholeWeekInd = 7
    res = cache.get(key)

    if res:
        for x in res:
            if PlacementState.objects.filter(campaign_id=campaign_id, placement_id=x['placement']):
                state = list(PlacementState.objects.filter(campaign_id=campaign_id, placement_id=x['placement']))[0]
                x['state'] = state.state
            else:
                x['state'] = 0
            x["analitics"] = mlFillPredictionAnswer(x["placement"], False, "kmeans", "ctr_cvr_cpc_cpm_cpa")
            x["analitics1"] = mlFillPredictionAnswer(x["placement"], False, "log" , "ctr_cvr_cpc_cpm_cpa")
        return res
    # no cache hit

    from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, tzinfo=utc)
    to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, tzinfo=utc)
    q = NetworkAnalyticsReport_ByPlacement.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=campaign_id,
        hour__gte=from_date,
        hour__lte=to_date,
    ).select_related(
        "Placement"
    ).values(
        'placement',
        'placement__rtbimpressiontrackerplacementdomain__domain'
    ).annotate(
        placement_name=F('placement_name'), #placement__name
        NetworkPublisher=Concat(F('publisher_name'),Value("/"), F('seller_member_name')),
        placementState=F('placement__state'),
        cost=Sum('cost'),
        conv=Sum('total_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
        imps_viewed=Sum('imps_viewed'),
        view_measured_imps=Sum('view_measured_imps'),
    ).annotate(
        cpc=Case(When(~Q(clicks=0), then=1.0 * F('cost') / F('clicks')), output_field=FloatField()),
        cpm=Case(When(~Q(imp=0), then=1.0 * F('cost') / F('imp') * 1000), output_field=FloatField()),
        cvr=Case(When(~Q(imp=0), then=100.0 * F('conv') / F('imp')), output_field=FloatField()),
        ctr=Case(When(~Q(imp=0), then=100.0 * F('clicks') / F('imp')), output_field=FloatField()),
        cpa=Case(When(~Q(conv=0), then=1.0 * F('cost') / F('conv')), output_field=FloatField()),
        view_rate=Case(When(~Q(view_measured_imps=0), then=100.0 * F('imps_viewed') / F('view_measured_imps')), output_field=FloatField()),
        view_measurement_rate=Case(When(~Q(imp=0), then=100.0 * F('view_measured_imps') / F('imp')), output_field=FloatField()),
    )
    res = list(q)
    for x in res:
        if PlacementState.objects.filter(campaign_id=campaign_id, placement_id=x['placement']):
            state = list(PlacementState.objects.filter(campaign_id=campaign_id, placement_id=x['placement']))[0]
            x['state'] = state.state
        else:
            x['state'] = 0
        x["analitics"] = mlFillPredictionAnswer(x["placement"], False, "kmeans", "ctr_cvr_cpc_cpm_cpa")
        x["analitics1"] = mlFillPredictionAnswer(x["placement"], False, "log", "ctr_cvr_cpc_cpm_cpa")
        x.pop('placementState', None)


    cache.set(key, res)
    return res


@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def campaignDomains(request, id):
    """
Get single campaign details by domains

## Url format: /api/v1/campaigns/:id/domains?from_date={from_date}&to_date={to_date}&skip={skip}&take={take}&sort={sort}&order={order}&filter={filter}&totalSummary={totalSummary}

+ Parameters
    + id (Number) - id for getting information about company
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
    + filter (string, optional) - devextreme JSON serialized filter

Field "placement" must contain name and id of placement. Id in parenthesis
    """

    params = parse_get_params(request.GET)
    if params['from_date'] > params['to_date']:
        params['from_date'], params['to_date'] = params['to_date'], params['from_date']
    res = get_campaign_placement(id, params['from_date'], params['to_date'])
    if params['filter']:
        filter_function = filter_func.get_filter_function(params['filter'])
        res = filter(filter_function, res)
    reverse_order = params['order'] == 'desc'
    allowed_key_names = set(
        ["placement", "NetworkPublisher", "placementState", "cost", "conv", "imp", "clicks", "cpc", "cpm", "cvr", "ctr", "cpa",
         'imps_viewed', 'view_measured_imps', 'view_rate', 'view_measurement_rate', "analitics"])
    key_name = params['sort']
    if 'sort' not in request.GET:
        key_name = 'imp'
        reverse_order = True
    if key_name not in allowed_key_names:
        key_name = 'placement'
    res.sort(key=lambda x: x[key_name], reverse=reverse_order)
    totalCount = len(res)

    result = {"data": res[params['skip']:params['skip'] + params['take']], "totalCount": totalCount}

    sums = reduce(make_sum, res, {"cost":0, "conv":0, "imp":0, "clicks":0, "imps_viewed":0, "view_measured_imps":0,
                                  "view_rate":0, "view_measurement_rate":0})
    sums['cpc'] = float(sums['cost']) / sums['clicks'] if sums['clicks'] else 0
    sums['cpa'] = float(sums["cost"]) / sums['conv'] if sums['conv'] else 0
    sums['view_rate'] = 100.0 * float(sums['imps_viewed']) / float(sums['view_measured_imps']) if sums[
        'view_measured_imps'] else 0
    sums['view_measurement_rate'] = 100.0 * float(sums['view_measured_imps']) / float(sums['imp']) if sums['imp'] else 0
    sums["cpm"] = 1000.0 * float(sums['cost'])/sums['imp'] if sums['imp'] else 0
    sums["cvr"] = float(sums['conv'])/sums['imp'] if sums['imp'] else 0
    sums['ctr'] = 100.0 * float(sums["clicks"]) / sums['imp'] if sums['imp'] else 0

    result['totalSummary'] = sums

    return Response(result)


def sum_for_data_and_percent(arr, group_others=False):
    arr.sort(key=lambda x: x['data'])
    s = sum(x['data'] for x in arr)
    for x in arr:
        x['data'] = 100.0 * x['data'] / s
    if group_others:
        # ind = bisect.bisect((x['data'] for x in arr) , 0.4)
        l = list(itertools.takewhile(lambda x: x['data'] < 0.5, arr))
        ind = len(l)
        new_arr = [{'section': 'Other', 'data': sum(x['data'] for x in arr[:ind])}]
        new_arr.extend(arr[ind:])
        return new_arr
    else:
        return arr


section_to_db = {
    'Placement': (NetworkAnalyticsReport_ByPlacement, "placement"),
    'creative_id': (NetworkAnalyticsReport_ByPlacement, "creative"),
    'creative_size': (NetworkAnalyticsReport_ByPlacement, "size"),
    # 'viewability'
    # 'OS':(SiteDomainPerformanceReport,"operating_system"),
    'OS': (NetworkDeviceReport_Simple, "operating_system"),
    'carrier': (NetworkCarrierReport_Simple, "carrier"),
    'network(seller)': (NetworkAnalyticsReport_ByPlacement, "seller_member"),
    'connection_type': (NetworkDeviceReport_Simple, "connection_type"),
    'device': (NetworkDeviceReport_Simple, "device_model"),
}


def get_campaign_detals(campaign_id, from_date, to_date, section):
    key = '_'.join(('rtb_campaign_detals', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'), section))
    res = cache.get(key)
    if res: return res
    field_name, _name,  q = get_section_query(campaign_id, from_date, to_date, section)
    # .annotate(
    #        ctr=Case(When(~Q(imp=0), then=F('clicks') / F('imp')), output_field=FloatField()),
    #    )
    results = list(q)
    if section=='Placement':
        for x in results:
            x[_name] = '{}/{}'.format(x[_name], x[field_name])
    views = sum_for_data_and_percent([{'section': x[_name], 'data': x['imp']} for x in results])
    conversions = sum_for_data_and_percent([{'section': x[_name], 'data': x['imp']} for x in results if x['conv']])
    res = {'all': views, 'conversions': conversions}
    cache.set(key, res)
    return res


def get_section_query(campaign_id, from_date, to_date, section):
    table_name, field_name = section_to_db.get(section)
    group_adv_fields = {
        'conv': Sum('total_convs'),
        'imp': Sum('imps'),
        'clicks': Sum('clicks'),
    }
    try:
        table_name._meta.get_field('cost')
        group_adv_fields['sum_cost']=Sum('cost')
    except:
        pass
    # if section=='OS':
    #     group_adv_fields['conv']=Sum('post_click_convs')+Sum('post_view_convs')
    group_fields = [field_name]
    name_for_field = field_name + '_name'
    try:
        table_name._meta.get_field(name_for_field)
        group_fields.append(name_for_field)
        _name = name_for_field
    except:
        _name = field_name
    filter_params = {'campaign_id': campaign_id}
    try:
        table_name._meta.get_field('hour')
        filter_params['hour__gte'] = from_date
        filter_params['hour__lte'] = to_date
    except:
        filter_params['day__gte'] = from_date
        filter_params['day__lte'] = to_date
    q = table_name.objects.filter(**filter_params).values(*group_fields).annotate(**group_adv_fields)
    return  field_name, _name, q


@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def campaignDetails(request, id):
    """
Get single campaign details for given period 

## Url format: /api/v1/campaigns/:id/details?from_date={from_date}&to_date={to_date}&section={section}

+ Parameters

    + id (Number) - id for selecting informations about company
    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    + section (string) - category for selecting imps
        + Format: string
        + Example: placement
For "all":
    field "section" - selected category (if category="placement"  then field "section" hold placement id),
    field "data" - impressions for this category values.
For "conversions":
    field "section" - selected category where conversion<>0 (if category="placement"  then field "section" hold placement id),
    field "data" - impressions for this category values.
    """
    params = parse_get_params(request.GET)
    res = get_campaign_detals(id, params['from_date'], params['to_date'], params['section'])
    return Response(res)


def get_cpa_buckets(campaign_id, from_date, to_date, section='Placement'):
    key = '_'.join(('rtb_cpa_buckets', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'), section))
    res = cache.get(key)
    if res: return res

    field_name, _name,  q = get_section_query(campaign_id, from_date, to_date, section)
    table = q.model
    #if table==NetworkAnalyticsReport_ByPlacement:
    if section=='Placement':
        q = q.annotate(
            placementid=F('placement_id'),
            placementname=F('placement__name'),
            sellerid=F('seller_member_id'),
            sellername=F('seller_member__name'),
        )
    q = q.annotate(
        cpa=Case(When(~Q(conv=0), then=F('sum_cost') / F('conv')), output_field=FloatField()),
    )
    q = q.filter(conv__gt=0)

    #
    # q = NetworkAnalyticsReport_ByPlacement.objects.filter(
    #     # advertiser_id=advertiser_id,
    #     campaign_id=campaign_id,
    #     hour__gte=from_date,
    #     hour__lte=to_date,
    # ).values(field_name).annotate(
    #     conv=Sum('total_convs'),
    #     sum_cost=Sum('cost'),
    #     placementid=F('placement_id'),
    #     placementname=F('placement__name'),
    #     sellerid=F('seller_member_id'),
    #     sellername=F('seller_member__name'),
    # ).annotate(
    #     cpa=Case(When(~Q(conv=0), then=F('sum_cost') / F('conv')), output_field=FloatField()),
    # ).filter(
    #     conv__gt=0
    # )

    # print q.query
    res = list(q)
    for x in res:
        x.pop('conv', None)
        x.pop('sum_cost', None)
    cache.set(key, res)
    return res


@api_view()
@check_user_advertiser_permissions(campaign_id_num=0)
def bucketsCPA(request, id):
    """
Get single campaign details for given period

## Url format: /api/v1/campaigns/:id/cpabuckets?from_date={from_date}&to_date={to_date}&category={category}

+ Parameters

    + id (Number) - id for selecting informations about company
    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    """
    params = parse_get_params(request.GET)
    res = get_cpa_buckets(id, params['from_date'], params['to_date'], params['category'])
    # convs
    return Response(res)

@api_view(['GET', 'POST'])
@check_user_advertiser_permissions(campaign_id_num=0)
def mlApiAnalitics(request, id):
    """
Post: commends the decision taken by the machine

## Url format: /api/v1/campaigns/:id/MLPlacement
    body {
        placementId: placementId,
        checked: checked
    }

+ Parameters
    + id (Number) - id company
    + placementId (Number) - placement id
    + checked (boolean) - true | false


http://localhost:3000/api/v1/campaigns/13921687/MLPlacement
{placementId: 3898, checked: true}


GET: diagramms for week for a placement
## Url format: /api/v1/campaigns/:id/MLPlacement?placementId={placementId}

+ Parameters
    + id (Number) - id company
	+ placementId (Number) - placement id
    """
    if request.method == "GET":
        res = mlApiWeeklyPlacementRecignition(request)
    if request.method == "POST":
        res = mlApiSaveExpertDecision(request)
    return res


    
def mlApiWeeklyPlacementRecignition(request):
    placement_id = request.GET.get("placementId")
    test_name = request.GET.get("test_name")
    test_type = request.GET.get("test_type")
    res = mlFillPredictionAnswer(placement_id, True, test_type, test_name)
    return Response(res)

def mlApiSaveExpertDecision(request):
    placement_id = request.GET.get("placementId")
    checked = request.GET.get("checked")
    test_type = request.GET.get("test_type")
    test_name = request.GET.get("test_name")
    day = request.GET.get("day")

    goodClusters = mlGetGoodClusters(test_name)

    test_number = mlGetTestNumber(test_type, test_name)
    if test_type == "kmeans":
        placementInfo = MLPlacementsClustersKmeans.objects.filter(
            placement_id=placement_id,
            day=day,
            test_number=test_number
        )
        if test_type == "log":
            pass #get info about

    decision = None
    if placementInfo.cluster == goodClusters[day]:
        if checked == True:
            decision = "good"
        else:
            decision = "bad"
    else:
        if checked == True:
            decision = "bad"
        else:
            decision = "good"
    expertMarkRecord = MLExpertsPlacementsMarks(
        placement_id=placement_id,
        day=day,
        expert_decision=decision,
        date=timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone())
    )
    try:
        tempQuery = MLExpertsPlacementsMarks.objects.filter(
            placement_id=placement_id,
            day=day
        )
        if not tempQuery:
            expertMarkRecord.save()
        else:
            tempQuery.update(
                expert_decision=decision,
                date=timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone())
            )
    except Exception, e:
        print "Can't save expert mark. Error: " + str(e)

    try:
        placementInfo.update(expert_decision=checked)
    except Exception, e:
        print "Can't save expert decision. Error: " + str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    res = mlFillPredictionAnswer(placement_id, False, test_type, test_name)#RETURN ONE DAYWEEK?
    return Response(res)

def mlFillPredictionAnswer(placement_id = 1, flagAllWeek = False, test_type = "kmeans", test_name = "ctr_viewrate"):
    if test_type == "kmeans":
        mlAnswer = mlGetPlacementInfoKmeans(placement_id, flagAllWeek, test_type, test_name)
        if flagAllWeek == False:
            wholeWeekInd = 7
            if mlAnswer == -1 or mlAnswer == -2:
                res = ({  # for one object
                    "good": mlAnswer,
                    "bad": mlAnswer,
                    "checked": mlAnswer
                })
                return res

            if str(wholeWeekInd) not in mlAnswer:  # for one object
                res = ({
                    "good": -3,
                    "bad": -3,
                    "checked": -3
                })
            else:
                res = ({
                    "good": mlAnswer[str(wholeWeekInd)]['good'],
                    "bad": mlAnswer[str(wholeWeekInd)]['bad'],
                    "checked": mlAnswer[str(wholeWeekInd)]['checked']
                })
            return res
        else:
            mlAnswer = mlGetPlacementInfoKmeans(placement_id, True, test_type, test_name)  # get data from recognition database
            res = []
            if mlAnswer == -1 or mlAnswer == -2:  # error with data in database
                for weekday in xrange(8):  # for all week, 8 - quantity of weekdays+whole week in mlAnswer
                    res.append({
                        "day": weekday,
                        "good": mlAnswer,
                        "bad": mlAnswer,
                        "checked": mlAnswer
                    })
                return res

            for weekday in xrange(8):  # 8 - quantity of weekdays+whole week in mlAnswer
                if str(weekday) not in mlAnswer:  # for array
                    res.append({
                        "day": weekday,
                        "good": -3,
                        "bad": -3,
                        "checked": -3
                    })
                else:
                    res.append({
                        "day": weekday,
                        "good": mlAnswer[str(weekday)]['good'],
                        "bad": mlAnswer[str(weekday)]['bad'],
                        "checked": mlAnswer[str(weekday)]['checked']
                    })
        return res
    #TODO getting results for logistic regression
    if test_type == "log":
        res = ({
            "good": -1,
            "bad": -1,
            "checked": -1
        })
        return res
    res = ({  # if wrong test type
        "good": -1,
        "bad": -1,
        "checked": -1
    })
    return res

@api_view(["GET"])
@check_user_advertiser_permissions(campaign_id_num=0)
def mlApiRandomTestSet(request):
    action = request.GET.get("action")
    if action == "create":
        placemetsDataQuery = MLViewFullPlacementsData.objects.raw(
            """
            SELECT
              placement_id as id,
              imps,
              clicks,
              total_convs,
              imps_viewed,
              view_measured_imps,
              sum_cost,
              cpa,
              ctr,
              cvr,
              cpc,
              cpm,
              view_rate,
              view_measurement_rate
            FROM
              ml_view_full_placements_data
            TABLESAMPLE BERNOULLI(20)
            limit 127;
            """
        )
        res = []
        for row in placemetsDataQuery:
            placement = {}
            placement["placement_id"] = row.id
            placement["imps"] = row.imps
            placement["clicks"] = row.clicks
            placement["total_convs"] = row.total_convs
            placement["imps_viewed"] = row.imps_viewed
            placement["view_measured_imps"] = row.view_measured_imps
            placement["sum_cost"] = float(row.sum_cost)
            placement["cpa"] = float(row.cpa)
            placement["ctr"] = float(row.ctr)
            placement["cvr"] = float(row.cvr)
            placement["cpc"] = float(row.cpc)
            placement["cpm"] = float(row.cpm)
            placement["view_rate"] = float(row.view_rate)
            placement["view_measurement_rate"] = float(row.view_measurement_rate)

            queryRes = NetworkAnalyticsReport_ByPlacement.objects.filter(
                placement_id=row.id
            ).select_related(
                "Placement"
            ).values(
                'placement',
                'placement__rtbimpressiontrackerplacementdomain__domain',
                'placement__mlexpertsplacementsmarks__expert_decision'
            ).annotate(
                placement_name=F('placement_name'),  # placement__name
                NetworkPublisher=Concat(F('publisher_name'), Value("/"), F('seller_member_name')),
            )

            if not queryRes:
                placement["domain"] = ""
                placement["placement_name"] = ""
                placement["publisher"] = ""
            else:
                placement["domain"] = queryRes[0]["placement__rtbimpressiontrackerplacementdomain__domain"]
                placement["placement_name"] = queryRes[0]["placement_name"]
                placement["publisher"] = queryRes[0]["NetworkPublisher"]
            res.append(placement)
        try:
            MLTestDataSet(
                data=res,
                created=timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone())
            ).save()
        except Exception, e:
            print "Can't save test set" + str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(res)

    if action == "send":
        try:
            max_date = MLTestDataSet.objects.latest("created")
            if not max_date:
                print "Can't get latest date"
                return Response(status=status.HTTP_400_BAD_REQUEST)
            res = MLTestDataSet.objects.filter(created=max_date.created).values("data")
            if not res:
                print "Can't get info"
                return Response(status=status.HTTP_400_BAD_REQUEST)
            for i in xrange(len(res[0]["data"])):
                queryRes = MLExpertsPlacementsMarks.objects.filter(placement_id=res[0]["data"][i]["placement_id"])
                if not queryRes:
                    res[0]["data"][i]["mark"] = None
                else:
                    res[0]["data"][i]["mark"] = queryRes[0].expert_decision
        except Exception, e:
            print "Error in sending test dataset " + str(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(res[0]["data"])

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@check_user_advertiser_permissions(campaign_id_num=0)
def mlApiSaveExpertPlacementMark(request):
    placement_id = request.GET.get("placementId")
    day = request.GET.get("day")
    decision = request.GET.get("decision")
    if not (decision == "good" or decision == "bad"):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    expertMarkRecord = MLExpertsPlacementsMarks(
        placement_id=placement_id,
        day=day,
        expert_decision=decision,
        date=timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone())
    )
    try:
        tempQuery = MLExpertsPlacementsMarks.objects.filter(
            placement_id=placement_id,
            day=day
        )
        if not tempQuery:
            expertMarkRecord.save()
        else:
            tempQuery.update(
                expert_decision=decision,
                date=timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone())
            )
    except Exception, e:
        print "Can't save expert mark. Error: " + str(e)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@check_user_advertiser_permissions(campaign_id_num=0)
def changeState(request, campaignId):
    """
    POST single campaign details by domains

    ## Url format: /api/v1/campaigns/:id/changestate

    + Parameters
        + id (Number) - id for putting information about company
        + placement (Number) - placement id
        + activeState (string) - Change state (white, black, suspend)
        + date - suspend date

    503 - Not connect to appnexus server
    404 - Not found

    """
    placementId = request.data.get("placement")
    activeState = request.data.get("activeState")   # 4 - white / 2 - black / 1 - suspend

    if request.data.get("activeState") == 1 and request.data.get("suspendTimes") is not None and request.data.get("suspendTimes") != "unlimited":
        date = datetime.date.fromtimestamp(int(request.data.get("suspendTimes")))
    else:
        date = None

    listObj = []

    try:
        if activeState == 0:
            placementStateInTable = list(PlacementState.objects\
                                         .filter(Q(campaign_id=campaignId), Q(placement_id__in=placementId)))
            for plState in placementStateInTable:
                obj, created = PlacementState.objects.update_or_create(campaign_id=campaignId,
                                                                   placement_id=plState.placement_id,
                                                                   defaults=dict(
                                                                       state=0,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))
            return Response('Unactive')
    except Exception as e:
        print e

    try:
        checkUnclick = False
        placementStateInTable = list(PlacementState.objects\
            .filter(Q(campaign_id=campaignId), Q(placement_id__in=placementId)))
        for plState in placementStateInTable:
            if plState.state != activeState:
                checkUnclick = False
                break
            else:
                checkUnclick = True
        if checkUnclick == True:
            for plState in placementStateInTable:
                obj, created = PlacementState.objects.update_or_create(campaign_id=campaignId,
                                                                   placement_id=plState.placement_id,
                                                                   defaults=dict(
                                                                       state=0,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))
            return Response('Unactive')
    except Exception as e:
        print e

    try:
        for i, placement in enumerate(placementId):
            obj, created = PlacementState.objects.update_or_create(campaign_id=campaignId,
                                                                   placement_id=placement,
                                                                   defaults=dict(
                                                                       state=activeState,
                                                                       suspend=date,
                                                                       change=True
                                                                   ))

            listObj.append({
                'placementId': obj.placement_id,
                'campaign_id': obj.campaign_id,
                'suspend': obj.suspend,
                'state': obj.state
            })
        return Response(listObj)
    except ValueError, e:
        return Response(str(e))


def getPlacementDomain(placementId):
    domains = RtbImpressionTrackerPlacement.objects.filter(placement_id=placementId)
    if not domains:
        return "", ""
    allDomains = ""
    for row in domains:
        if row.domain != "null":
            allDomains += (str(row.domain) + "; ")
    if allDomains != "":
        allDomains = allDomains[:-2]
    domain = RtbImpressionTrackerPlacementDomain.objects.filter(placement_id=placementId)
    if not domain:
        return allDomains, ""
    domain = domain[0].domain
    return allDomains, domain

@api_view(["GET"])
@check_user_advertiser_permissions(campaign_id_num=0)
def mlApiCalcAUC(request):
    test_type = request.GET.get("test_type")
    test_name = request.GET.get("test_name")
    res = mlCalcAuc(test_type, test_name)
    return Response(res)

@api_view(['GET', 'POST'])
@check_user_advertiser_permissions(campaign_id_num=0)
def ApiCampaignRules(request, id):#return/save campaign's rules
    if request.method == "GET":
        res = getCampaignRules(request, id)#return
    if request.method == "POST":
        res = saveCampaignRules(request, id)#save
    return res

def getCampaignRules(request, id):
    try:
        rules = CampaignRules.objects.get(campaign_id=id)
    except Exception, e:
        res = []
        return Response(res)
    res = rules.rules
    return Response(res)

def saveCampaignRules(request, id):
    rule = request.data.get("ruleObj")
    try:
        CampaignRules.objects.update_or_create(
            campaign_id=id,
            defaults={"rules":rule})
    except Exception, e:
        print "Error in inserting/updating campaign rules: ", str(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    res = {}
    res["campaign_id"] = id
    res["rule"] = rule
    return Response(res)