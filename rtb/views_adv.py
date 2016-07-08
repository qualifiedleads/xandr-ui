from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response


@api_view()
def singleCampaign(request, id):
    """
Get campaign name by id

## Url format: /api/v1/campaigns/:id

+ Parameters

    + id(Number) - id for getting information about company

    """
    return Response({
        "id": 19,
        "campaign": "first campaign"
    })


@api_view()
def graphInfo(request, id):
    """
Get single campaign statistics data for given period by selected categories: impression, cpa, cpc, clicks, mediaspent, conversions, ctr

## Url format: /api/v1/campaigns/:id/graphinfo/?from_date={from_date}&to_date={to_date}&by={by}

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
    return Response([
        {'date': "2016-06-'27T00':'00':00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': -5, 'mediaspent': 5,
         'conversions': 40,
         'ctr': 15},
        {'date': "2016-06-'28T00':'00':00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 1, 'mediaspent': 15,
         'conversions': 23,
         'ctr': -10},
        {'date': "2016-06-'29T00':'00':00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 2, 'mediaspent': 5,
         'conversions': 33,
         'ctr': 10},
        {'date': "2016-06-'30T00':'00':00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': 6, 'mediaspent': 55,
         'conversions': 87,
         'ctr': -42},
        {'date': "2016-07-'01T00':'00':00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': 9, 'mediaspent': 44,
         'conversions': -20,
         'ctr': -57},
        {'date': "2016-07-'02T00':'00':00Z", 'impression': 10, 'cpa': 10, 'cpc': 15, 'clicks': 8, 'mediaspent': 77,
         'conversions': 23,
         'ctr': 99},
        {'date': "2016-07-'03T00':'00':00Z", 'impression': 30, 'cpa': 50, 'cpc': 13, 'clicks': 23, 'mediaspent': 66,
         'conversions': -10,
         'ctr': 110},
        {'date': "2016-07-'04T00':'00':00Z", 'impression': 40, 'cpa': 50, 'cpc': 14, 'clicks': 12, 'mediaspent': 11,
         'conversions': 37,
         'ctr': 56},
        {'date': "2016-07-'05T00':'00':00Z", 'impression': 50, 'cpa': 90, 'cpc': 90, 'clicks': -10, 'mediaspent': 99,
         'conversions': 50,
         'ctr': 67},
        {'date': "2016-07-'06T00':'00':00Z", 'impression': 40, 'cpa': 175, 'cpc': 120, 'clicks': 31, 'mediaspent': -11,
         'conversions': 23,
         'ctr': 67},
        {'date': "2016-07-'07T00':'00':00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 70, 'mediaspent': -2,
         'conversions': 58,
         'ctr': -20},
        {'date': "2016-07-'08T00':'00':00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 26, 'mediaspent': 5,
         'conversions': 21,
         'ctr': -10},
        {'date': "2016-07-'09T00':'00':00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 52, 'mediaspent': 76,
         'conversions': 10,
         'ctr': 70},
        {'date': "2016-07-'10T00':'00':00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 1, 'mediaspent': 32,
         'conversions': 49,
         'ctr': 90},
        {'date': "2016-07-'11T00':'00':00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 38, 'mediaspent': 11,
         'conversions': 99,
         'ctr': 10},
        {'date': "2016-07-'12T00':'00':00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': -16, 'mediaspent': 15,
         'conversions': 60,
         'ctr': 58},
        {'date': "2016-07-'13T00':'00':00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': -40, 'mediaspent': 46,
         'conversions': 23,
         'ctr': 78},
        {'date': "2016-07-'14T00':'00':00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': 24, 'mediaspent': 68,
         'conversions': -20,
         'ctr': 80},
        {'date': "2016-07-'15T00':'00':00Z", 'impression': 10, 'cpa': 10, 'cpc': 15, 'clicks': 12, 'mediaspent': 49,
         'conversions': -37,
         'ctr': 22},
        {'date': "2016-07-'16T00':'00':00Z", 'impression': 30, 'cpa': 100, 'cpc': 13, 'clicks': 83, 'mediaspent': 36,
         'conversions': -1,
         'ctr': 67},
        {'date': "2016-07-'17T00':'00':00Z", 'impression': 40, 'cpa': 110, 'cpc': 14, 'clicks': 41, 'mediaspent': 28,
         'conversions': 65,
         'ctr': -10},
        {'date': "2016-07-'18T00':'00':00Z", 'impression': 50, 'cpa': 90, 'cpc': 90, 'clicks': 27, 'mediaspent': 95,
         'conversions': 23,
         'ctr': 88},
        {'date': "2016-07-'19T00':'00':00Z", 'impression': 40, 'cpa': 95, 'cpc': 120, 'clicks': 83, 'mediaspent': 92,
         'conversions': 10,
         'ctr': 77},
        {'date': "2016-07-'20T00':'00':00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': -20, 'mediaspent': 15,
         'conversions': 7,
         'ctr': 66},
        {'date': "2016-07-'21T00':'00':00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 56, 'mediaspent': 54,
         'conversions': 34,
         'ctr': -10},
        {'date': "2016-07-'22T00':'00':00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 17, 'mediaspent': 22,
         'conversions': 65,
         'ctr': -40},
        {'date': "2016-07-'23T00':'00':00Z", 'impression': -12, 'cpa': 10, 'cpc': 32, 'clicks': 22, 'mediaspent': 77,
         'conversions': 52,
         'ctr': -70},
        {'date': "2016-07-'24T00':'00':00Z", 'impression': -32, 'cpa': 30, 'cpc': 12, 'clicks': 29, 'mediaspent': 90,
         'conversions': 23,
         'ctr': -54},
        {'date': "2016-07-'25T00':'00':00Z", 'impression': -20, 'cpa': 20, 'cpc': 30, 'clicks': 90, 'mediaspent': 17,
         'conversions': 59,
         'ctr': 28},
        {'date': "2016-07-'26T00':'00':00Z", 'impression': -39, 'cpa': 50, 'cpc': 19, 'clicks': 45, 'mediaspent': 47,
         'conversions': 82,
         'ctr': 65},
        {'date': "2016-07-'27T00':'00':00Z", 'impression': -10, 'cpa': 10, 'cpc': 15, 'clicks': -30, 'mediaspent': 32,
         'conversions': 33,
         'ctr': 58}
    ])


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
    return Response([{
        "Date": "03/12/2013",
        "Open": "827.90",
        "High": "830.69",
        "Low": "822.31",
        "Close": "825.31",
        "Volume": "1641413"
    }, {
        "Date": "03/13/2013",
        "Open": "826.99",
        "High": "826.99",
        "Low": "817.39",
        "Close": "821.54",
        "Volume": "1651111"
    }, {
        "Date": "03/14/2013",
        "Open": "818.50",
        "High": "820.30",
        "Low": "813.34",
        "Close": "814.30",
        "Volume": "3099791"
    }, {
        "Date": "03/17/2013",
        "Open": "805.00",
        "High": "812.76",
        "Low": "801.47",
        "Close": "807.79",
        "Volume": "1838552"
    }, {
        "Date": "03/18/2013",
        "Open": "811.24",
        "High": "819.25",
        "Low": "806.45",
        "Close": "811.32",
        "Volume": "2098176"

    }, {
        "Date": "03/19/2013",
        "Open": "816.83",
        "High": "817.51",
        "Low": "811.44",
        "Close": "814.71",
        "Volume": "1464122"
    }, {
        "Date": "03/20/2013",
        "Open": "811.29",
        "High": "816.92",
        "Low": "809.85",
        "Close": "811.26",
        "Volume": "1477590"
    }, {
        "Date": "03/21/2013",
        "Open": "814.74",
        "High": "815.24",
        "Low": "809.64",
        "Close": "810.31",
        "Volume": "1491678"
    }, {
        "Date": "03/24/2013",
        "Open": "812.41",
        "High": "819.23",
        "Low": "806.82",
        "Close": "809.64",
        "Volume": "1712684"
    }, {
        "Date": "03/25/2013",
        "Open": "813.50",
        "High": "814.00",
        "Low": "807.79",
        "Close": "812.42",
        "Volume": "1191912"
    }])


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
        'all': [
            {
                'section': "Android",
                'data': 60
            },
            {
                'section': "iOs",
                'data': 30
            },
            {
                'section': "Windows",
                'data': 10
            }
        ],
        'conversions': [
            {
                'section': "Android",
                'data': 23
            },
            {
                'section': "iOs",
                'data': 72
            },
            {
                'section': "Windows",
                'data': 5
            }
        ],
        'cpabuckets': {
            "cnn.com": "34.12",
            "lion.com": "3.76",
            "tiger.com": "7.97",
            "cat.com": "1.23",
            "dog.com": "16.11",
            "mouse.com": "6.53",
            "rabbit.com": "0.91",
            "bear.com": "1.9",
            "snake.com": "3.7",
            "squirrel.com": "4.78",
            "hamster.com": "0.62"
        }
    })
