from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from django.http import JsonResponse
from utils import parse_get_params, make_sum
from models import SiteDomainPerformanceReport, Campaign, GeoAnaliticsReport, NetworkAnalyticsReport
from django.db.models import Sum, Min, Max, Avg, Value, When, Case, F, Q, Func
from django.db.models.functions import Coalesce
from django.core.cache import cache
import itertools
import datetime
from pytz import utc


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
    return Response([
        {'date': "2016-06-27T00:00:00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': -5, 'mediaspent': 5,
         'conversions': 40, 'ctr': 15},
        {'date': "2016-06-28T00:00:00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 1, 'mediaspent': 15,
         'conversions': 23, 'ctr': -10},
        {'date': "2016-06-29T00:00:00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 2, 'mediaspent': 5,
         'conversions': 33, 'ctr': 10},
        {'date': "2016-06-30T00:00:00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': 6, 'mediaspent': 55,
         'conversions': 87, 'ctr': -42},
        {'date': "2016-07-01T00:00:00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': 9, 'mediaspent': 44,
         'conversions': -20, 'ctr': -57},
        {'date': "2016-07-02T00:00:00Z", 'impression': 10, 'cpa': 10, 'cpc': 15, 'clicks': 8, 'mediaspent': 77,
         'conversions': 23, 'ctr': 99},
        {'date': "2016-07-03T00:00:00Z", 'impression': 30, 'cpa': 50, 'cpc': 13, 'clicks': 23, 'mediaspent': 66,
         'conversions': -10, 'ctr': 110},
        {'date': "2016-07-04T00:00:00Z", 'impression': 40, 'cpa': 50, 'cpc': 14, 'clicks': 12, 'mediaspent': 11,
         'conversions': 37, 'ctr': 56},
        {'date': "2016-07-05T00:00:00Z", 'impression': 50, 'cpa': 90, 'cpc': 90, 'clicks': -10, 'mediaspent': 99,
         'conversions': 50, 'ctr': 67},
        {'date': "2016-07-06T00:00:00Z", 'impression': 40, 'cpa': 175, 'cpc': 120, 'clicks': 31, 'mediaspent': -11,
         'conversions': 23, 'ctr': 67},
        {'date': "2016-07-07T00:00:00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 70, 'mediaspent': -2,
         'conversions': 58, 'ctr': -20},
        {'date': "2016-07-08T00:00:00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 26, 'mediaspent': 5,
         'conversions': 21, 'ctr': -10},
        {'date': "2016-07-09T00:00:00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 52, 'mediaspent': 76,
         'conversions': 10, 'ctr': 70},
        {'date': "2016-07-10T00:00:00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 1, 'mediaspent': 32,
         'conversions': 49, 'ctr': 90},
        {'date': "2016-07-11T00:00:00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 38, 'mediaspent': 11,
         'conversions': 99, 'ctr': 10},
        {'date': "2016-07-12T00:00:00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': -16, 'mediaspent': 15,
         'conversions': 60, 'ctr': 58},
        {'date': "2016-07-13T00:00:00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': -40, 'mediaspent': 46,
         'conversions': 23, 'ctr': 78},
        {'date': "2016-07-14T00:00:00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': 24, 'mediaspent': 68,
         'conversions': -20, 'ctr': 80},
        {'date': "2016-07-15T00:00:00Z", 'impression': 10, 'cpa': 10, 'cpc': 15, 'clicks': 12, 'mediaspent': 49,
         'conversions': -37, 'ctr': 22},
        {'date': "2016-07-16T00:00:00Z", 'impression': 30, 'cpa': 100, 'cpc': 13, 'clicks': 83, 'mediaspent': 36,
         'conversions': -1, 'ctr': 67},
        {'date': "2016-07-17T00:00:00Z", 'impression': 40, 'cpa': 110, 'cpc': 14, 'clicks': 41, 'mediaspent': 28,
         'conversions': 65, 'ctr': -10},
        {'date': "2016-07-18T00:00:00Z", 'impression': 50, 'cpa': 90, 'cpc': 90, 'clicks': 27, 'mediaspent': 95,
         'conversions': 23, 'ctr': 88},
        {'date': "2016-07-19T00:00:00Z", 'impression': 40, 'cpa': 95, 'cpc': 120, 'clicks': 83, 'mediaspent': 92,
         'conversions': 10, 'ctr': 77},
        {'date': "2016-07-20T00:00:00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': -20, 'mediaspent': 15,
         'conversions': 7, 'ctr': 66},
        {'date': "2016-07-21T00:00:00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 56, 'mediaspent': 54,
         'conversions': 34, 'ctr': -10},
        {'date': "2016-07-22T00:00:00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 17, 'mediaspent': 22,
         'conversions': 65, 'ctr': -40},
        {'date': "2016-07-23T00:00:00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 22, 'mediaspent': 77,
         'conversions': 52, 'ctr': -70},
        {'date': "2016-07-24T00:00:00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 29, 'mediaspent': 90,
         'conversions': 23, 'ctr': -54},
        {'date': "2016-07-25T00:00:00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 90, 'mediaspent': 17,
         'conversions': 59, 'ctr': 28},
        {'date': "2016-07-26T00:00:00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': 45, 'mediaspent': 47,
         'conversions': 82, 'ctr': 65},
        {'date': "2016-07-27T00:00:00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': -30, 'mediaspent': 32,
         'conversions': 33, 'ctr': 58}
    ])


def calc_cpa(obj):
    return obj


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
    q = NetworkAnalyticsReport.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=campaign_id,
        hour__gte=from_date,
        hour__lte=to_date,
    ).values('hour').annotate(  # impression, cpa, cpc, clicks, mediaspent, conversions, ctr
        sum_cost=Sum('cost'),
        convs=Sum('total_convs'),
        # cpa = Case(When(Sum('total_convs'), then=Sum('media_cost')/Sum('total_convs')))
    ).annotate(
        cpa=Case(When(~Q(convs=0), then=F('sum_cost') / F('convs'))),
        date=Func(Value("'day'"), 'hour', function="date_trunc")
    ).order_by("hour")
    # values("date").annotate(
    #     low=Min("cpa"),
    #     high=Max("cpa"),
    #     avg=Avg("cpa")
    # )
    print q.query
    # first, last = None, None
    res = []
    key_func = lambda x: x["cpa"]
    for key, g in itertools.groupby(q, lambda x: x["date"]):
        group = list(g)
        try:
            avg = sum(itertools.imap(lambda x: x["sum_cost"], group)) / sum(itertools.imap(lambda x: x["convs"], group))
        except:
            avg = None
        res.append({
            "date": key,
            "low": min(group, key_func)["cpa"],
            "high": max(group, key_func)["cpa"],
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
    # return Response(res)
    return Response([
        {"date": "2016-06-19T00:00:00Z", "low": 24.00, "high": 25.00, "open": 25.00, "close": 24.875, "avg": 24.5},
        {"date": "2016-06-20T00:00:00Z", "low": 23.625, "high": 25.125, "open": 24.00, "close": 24.875, "avg": 24.375},
        {"date": "2016-06-21T00:00:00Z", "low": 26.25, "high": 28.25, "open": 26.75, "close": 27.00, "avg": 27.25},
        {"date": "2016-06-22T00:00:00Z", "low": 26.50, "high": 27.875, "open": 26.875, "close": 27.25, "avg": 27.1875},
        {"date": "2016-06-23T00:00:00Z", "low": 26.375, "high": 27.50, "open": 27.375, "close": 26.75, "avg": 26.9375},
        {"date": "2016-06-24T00:00:00Z", "low": 25.75, "high": 26.875, "open": 26.75, "close": 26.00, "avg": 26.3125},
        {"date": "2016-06-25T00:00:00Z", "low": 25.75, "high": 26.75, "open": 26.125, "close": 26.25, "avg": 25.9375},
        {"date": "2016-06-26T00:00:00Z", "low": 25.75, "high": 26.375, "open": 26.375, "close": 25.875, "avg": 26.0625},
        {"date": "2016-06-27T00:00:00Z", "low": 24.875, "high": 26.125, "open": 26.00, "close": 25.375, "avg": 25.5},
        {"date": "2016-06-28T00:00:00Z", "low": 25.125, "high": 26.00, "open": 25.625, "close": 25.75, "avg": 25.5625},
        {"date": "2016-06-29T00:00:00Z", "low": 25.875, "high": 26.625, "open": 26.125, "close": 26.375, "avg": 26.25},
    ])


def get_campaign_placement(advertiser_id, campaign_id, from_date, to_date):
    key = '_'.join(('rtb_campaign_placement', str(advertiser_id), str(campaign_id), from_date.strftime('%Y-%m-%d'),
                    to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res: return res
    # no cache hit
    from_date = datetime.datetime(from_date.year, from_date.month, from_date.day, tzinfo=utc)
    to_date = datetime.datetime(to_date.year, to_date.month, to_date.day, 23, tzinfo=utc)
    q = NetworkAnalyticsReport.objects.filter(
        # advertiser_id=advertiser_id,
        campaign_id=campaign_id,
        hour__gte=from_date,
        hour__lte=to_date,
    ).values('placement').annotate(  # impression, cpa, cpc, clicks, mediaspent, conversions, ctr
        sum_cost=Sum('cost'),
        convs=Sum('total_convs'),
        imp="5500",
        clicks="21",

        # cpa = Case(When(Sum('total_convs'), then=Sum('media_cost')/Sum('total_convs')))
    ).annotate(
        cpa=Case(When(~Q(convs=0), then=F('sum_cost') / F('convs'))),
        date=Func(Value("'day'"), 'hour', function="date_trunc")
    )
    print q.query
    res = []
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


    """
    return Response([{
        "placement": "CNN.com",
        "NetworkPublisher": "Google Adx",
        "conv": "8",
        "imp": "5500",
        "clicks": "21",
        "cpc": "$0,31",
        "cpm": "$1,38",
        "cvr": "",
        "ctr": "",
        "state": {
            "whiteList": "true",
            "blackList": "false",
            "suspended": "false"
        }
    },
        {
            "placement": "Hidden",
            "NetworkPublisher": "PubMatic",
            "conv": "3",
            "imp": "5500",
            "clicks": "21",
            "cpc": "$0,31",
            "cpm": "$1,38",
            "cvr": "",
            "ctr": "",
            "state": {
                "whiteList": "false",
                "blackList": "true",
                "suspended": "false"
            }
        },
        {
            "placement": "BBC.com",
            "NetworkPublisher": "OpenX",
            "conv": "1",
            "imp": "5500",
            "clicks": "21",
            "cpc": "$0,31",
            "cpm": "$1,38",
            "cvr": "",
            "ctr": "",
            "state": {
                "whiteList": "false",
                "blackList": "false",
                "suspended": "true"
            }
        },
        {
            "placement": "msn.com",
            "NetworkPublisher": "Rubicon",
            "conv": "8",
            "imp": "5500",
            "clicks": "21",
            "cpc": "$0,31",
            "cpm": "$1,38",
            "cvr": "",
            "ctr": "",
            "state": {
                "whiteList": "true",
                "blackList": "false",
                "suspended": "false"
            }
        }
    ])


@api_view()
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
    + section (string) - statistic fields to select (select every field if param is empty)
        + Format: string
        + Example: placement


    """
    return Response({
        'all': [{
            'section': "Android",
            'data': 60
        }, {
            'section': "iOs",
            'data': 30
        }, {
            'section': "Windows",
            'data': 10
        }],
        'conversions': [{
            'section': "Android",
            'data': 23
        }, {
            'section': "iOs",
            'data': 72
        }, {
            'section': "Windows",
            'data': 5
        }]
    })


@api_view()
def bucketsCPA(request):
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
    return Response([
        {
            "cpa": 1.2,
            "sellerid": 123,
            "sellername": "Rovio",
            "placementid": 234,
            "placementname": "AngryBirds"
        },
        {
            "cpa": 0.4,
            "sellerid": 678,
            "sellername": "Paris",
            "placementid": 9789,
            "placementname": "Cat"
        },
        {
            "cpa": 10.1,
            "sellerid": 3453,
            "sellername": "France",
            "placementid": 2325,
            "placementname": "Tom"
        },
        {
            "cpa": 4.1,
            "sellerid": 545,
            "sellername": "Lipton",
            "placementid": 111,
            "placementname": "Mouse"
        },
        {
            "cpa": 0.8,
            "sellerid": 35,
            "sellername": "River",
            "placementid": 45,
            "placementname": "Tributary"
        },
        {
            "cpa": 9.3,
            "sellerid": 90,
            "sellername": "Wood",
            "placementid": 3545,
            "placementname": "Land"
        },
        {
            "cpa": 2.4,
            "sellerid": 222,
            "sellername": "Pen",
            "placementid": 333,
            "placementname": "Gear"
        },
        {
            "cpa": 5.4,
            "sellerid": 54,
            "sellername": "World",
            "placementid": 3444454,
            "placementname": "Flower"
        },
        {
            "cpa": 6.1,
            "sellerid": 888,
            "sellername": "Bird",
            "placementid": 999,
            "placementname": "Kitten"
        },
        {
            "cpa": 13.1,
            "sellerid": 444,
            "sellername": "Dreams",
            "placementid": 56656,
            "placementname": "Sweet"
        },
        {
            "cpa": 0.1,
            "sellerid": 787,
            "sellername": "Hotel",
            "placementid": 76876,
            "placementname": "California"
        },
        {
            "cpa": 1.9,
            "sellerid": 678678,
            "sellername": "Star",
            "placementid": 12312,
            "placementname": "Sky"
        }
    ])
