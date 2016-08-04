from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.http import JsonResponse
from utils import parse_get_params, make_sum
from models import SiteDomainPerformanceReport, Campaign, GeoAnaliticsReport, NetworkAnalyticsReport_ByPlacement, Placement
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func, FloatField
from django.db.models.functions import Coalesce
from django.core.cache import cache
import itertools
import datetime
from pytz import utc
import filter_func


@api_view()
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
        "day":obj["day"],
        "cpa": None, "cpc": None, "ctr": None,
        "clicks": obj["clicks"],
        "mediaspent": obj["mediaspent"],
        "impression": obj["impression"],
    }
    try:
        post_click_convs = obj['post_click_convs'] or 0
        post_view_convs = obj['post_view_convs'] or 0
        res['conversions'] = post_click_convs + post_view_convs
        res['cpc'] = float(obj['mediaspent']) / obj['clicks'] if obj['clicks'] else 0
        res['cpa'] = float(obj["mediaspent"]) / res['conversions'] if res['conversions'] else 0
        res['ctr'] = float(obj["clicks"]) / obj['impression'] if obj['impression'] else 0
    except:
        pass
    return res


def get_campaign_data(advertiser_id, campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign', str(advertiser_id), str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id=advertiser_id,
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
    ).order_by('day')
    print q.query
    res = map(calc_another_fields, q)
    cache.set(key, res)
    return res


@api_view()
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
    advertiser_id = c.advertiser_id
    params = parse_get_params(request.GET, ["impression", "cpa", "cpc", "clicks", "mediaspent", "conversions", "ctr"])
    res = get_campaign_data(advertiser_id, id, params['from_date'], params['to_date'])
    return Response(res)
    # TODO: delete

def get_campaign_cpa(advertiser_id, campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign_candle', str(advertiser_id), str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    # from_date -= datetime.timedelta(days=1)
    # from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, 23, tzinfo = utc)
    from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, tzinfo=utc)
    to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, tzinfo=utc)
    q = NetworkAnalyticsReport_ByPlacement.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=campaign_id,
        hour__gte=from_date,
        hour__lte=to_date,
    ).values('hour').annotate(
        sum_cost=Sum('cost'),
        convs=Sum('total_convs'),
        # date=Func(Value("'day'"), 'hour', function="date_trunc")
    ).annotate(
        cpa=Case(When(~Q(convs=0), then=F('sum_cost') / F('convs')),output_field=FloatField()),
    )#.order_by("hour")
    # values("date").annotate(
    #     low=Min("cpa"),
    #     high=Max("cpa"),
    #     avg=Avg("cpa")
    # )
    # first, last = None, None
    res = []
    key_func = lambda x: x["cpa"]
    for key, g in itertools.groupby(q, lambda x: x["hour"].date()):
        group = list(g)
        try:
            avg = sum(itertools.imap(lambda x: x["sum_cost"], group)) / sum(itertools.imap(lambda x: x["convs"], group))
        except:
            avg = None
        min_val = min(group, key=key_func)
        max_val = max(group, key=key_func)
        res.append({
            "date": key,
            "low":  min_val["cpa"],
            "high": max_val["cpa"],
            "open": group[0]["cpa"],
            "close": group[-1]["cpa"],
            "avg": avg,
        })
    cache.set(key, res)
    return res


@api_view()
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
    res = get_campaign_cpa(advertiser_id, id, params['from_date'], params['to_date'])
    return Response(res)


def get_campaign_placement(campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign_placement', str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, tzinfo=utc)
    to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, tzinfo=utc)
    q = NetworkAnalyticsReport_ByPlacement.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=campaign_id,
        hour__gte=from_date,
        hour__lte=to_date,
    ).values('placement_id').annotate(
        placement = F('placement__name'),
        NetworkPublisher = F('placement__publisher__name'),
        placementState = F('placement__state'),
        cost=Sum('cost'),
        conv=Sum('total_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
    ).annotate(
        cpc=Case(When(~Q(clicks=0), then=F('cost') / F('clicks')), output_field=FloatField()),
        cpm=Case(When(~Q(imp=0), then=F('cost') / F('imp') *1000), output_field=FloatField()),
        cvr=Case(When(~Q(imp=0), then=F('conv') / F('imp')), output_field=FloatField()),
        ctr=Case(When(~Q(imp=0), then=F('clicks') / F('imp')), output_field=FloatField()),
    )
    res=list(q)
    for x in res:
        if x['placement'] is None:
            x['placement'] = 'Hidden ({})'.format(x['placement_id'])
        else:
            x['placement'] = '{} ({})'.format(x['placement'],x['placement_id'])
        if x['NetworkPublisher'] is None:
            #x['NetworkPublisher'] = 'Hidden publisher({})'.format(x['placement__publisher_id']) # this field not exist
            x['NetworkPublisher'] = 'Hidden publisher'
        x['state']={
            "whiteList": "true",
            "blackList": "false",
            "suspended": x['placementState']=='inactive'
        }
        x.pop('placement_id', None)
        x.pop('placementState', None)
    cache.set(key, res)
    return res

@api_view()
def campaignDomains(request, id):
    """
Get single campaign details by domains

## Url format: /api/v1/campaigns/:id/domains?from_date={from_date}&to_date={to_date}&skip={skip}&take={take}&sort={sort}&order={order}&filter={filter}

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
    allowed_key_names = set(["placement", "NetworkPublisher", "placementState", "cost", "conv", "imp", "clicks", "cpc", "cpm", "cvr", "ctr"])
    key_name = params['sort']
    if key_name not in allowed_key_names:
        key_name='placement'
    res.sort(key=lambda x: x[key_name], reverse=reverse_order)
    totalCount = len(res)
    res = res[params['skip']:params['skip'] + params['take']]
    result = { "data": res, "totalCount": totalCount}
    return Response(result)


@api_view()
def campaignDetails(request, id):
    """
Get single campaign details for given period 

## Url format: /api/v1/campaigns/:id/details?from_date={from_date}&to_date={to_date}&category={category}

+ Parameters

    + id (Number) - id for selecting informations about company
    + from_date (date) - Date to select statistics from
        + Format: Unixtime
        + Example: 1466667274
    + to_date (date) - Date to select statistics to
        + Format: Unixtime
        + Example: 1466667274
    + category (string) - category for selecting imps
        + Format: string
        + Example: placement
For "all":
    field "section" - selected category (if category="placement"  then field "section" hold placement id),
    field "data" - impressions for this category values.
For "conversions":
    field "section" - selected category where conversionR<>0 (if category="placement"  then field "section" hold placement id),
    field "data" - impressions for this category values.
    """
    # TODO This dictionary need to fill with names of all grouping sections
    section_to_field={
        'Placement':"placement"
    }
    # curl 'http://127.0.0.1:8000/api/v1/campaigns/13412702/details?from_date=1467320400&section=Placement&to_date=1469032344' --1.0 -H 'Host: 127.0.0.1:8000' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://127.0.0.1:8000/client/index.html' -H 'Cookie: csrftoken=tzdunvIQ55Ba7maBdr8WYeEW58S75rCn' -H 'Connection: keep-alive'
    params = parse_get_params(request.GET)
    field_name = section_to_field.get(params['section'],'placement')
    q = NetworkAnalyticsReport_ByPlacement.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=id,
        hour__gte=params['from_date'],
        hour__lte=params['to_date'],
    ).values(field_name).annotate(
        conv=Sum('total_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
    )#.annotate(
#        ctr=Case(When(~Q(imp=0), then=F('clicks') / F('imp')), output_field=FloatField()),
#    )
    results= list(q)
    if field_name == 'placement':
        placement_ids = set (x['placement'] for x in results)
        placements = Placement.objects.filter(pk__in=placement_ids)
        placement_names = {p['id']:p['name'] for p in placements}
        for x in results:
            x['placement']=placement_names.get(x['placement'], 'Hidden placement ({})'.format(x['placement']))
    views = [{'section':x[field_name],'data':x['imp']} for x in results]
    conversions = [{'section':x[field_name],'data':x['imp']} for x in results if x['conv']]
    return Response({'all':views,'conversions':conversions})

@api_view()
def bucketsCPA(request,id):
    """
Get single campaign details for given period

## Url format: /api/v1/campaigns/:id/cpabuckets?from_date={from_date}&to_date={to_date}&targetcpa={targetcpa}

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
    field_name = 'placement'
    #field_name = 'placement__site'
    # field_name='placement'
    q = NetworkAnalyticsReport_ByPlacement.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=id,
        hour__gte=params['from_date'],
        hour__lte=params['to_date'],
    ).values(field_name).annotate(
        conv=Sum('total_convs'),
        sum_cost=Sum('cost'),
        placementid=F('placement_id'),
        placementname=F('placement__name'),
        sellerid=F('seller_member_id'),
        sellername=F('seller_member__name'),
    ).annotate(
        cpa=Case(When(~Q(conv=0), then=F('sum_cost') / F('conv')), output_field=FloatField()),
    )
    res = list(q)
    for x in res:
        x.pop('conv', None)
        x.pop('sum_cost', None)
    # convs
    return Response(res)
