import itertools, time, datetime, re
from urllib import addbase

from django.http import JsonResponse
from django.db.models import Avg, Count, Sum
from models import SiteDomainPerformanceReport, Campaign
from django.core.cache import cache
from pytz import utc
import operator
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

def to_unix_timestamp(d):
    return str(int(time.mktime(d.timetuple())))


def calc_another_fields(obj):
    res = {}
    res.update(obj)
    res['conv'] = (obj.get('conv', 0) or 0) + (obj.get('conv_click', 0) or 0) + (obj.get('conv_view', 0) or 0)
    res['cpc'] = obj['spend'] / obj['clicks'] if obj['clicks'] else 0
    res['cpm'] = obj["spend"] / obj['imp'] * 1000 if obj['imp'] else 0
    res['cvr'] = res["conv"] / obj['imp'] if obj['imp'] else 0
    res['ctr'] = obj["clicks"] / obj['imp'] if obj['imp'] else 0
    res.pop('conv_click', None)
    res.pop('conv_view', None)
    res.pop('campaign', None)

    return res


def make_sum(dict1, dict2):
    res = {}
    for k in dict1:
        try:
            res[k] = dict1.get(k, 0) + dict2.get(k, 0)
        except:
            res[k] = dict1[k]
    return res

def get_campaigns_data(advertiser_id, from_date, to_date):
    key = '_'.join(('rtb_campaigns',str(advertiser_id), from_date.strftime('%Y-%m-%d'),to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res:return res
    #no cache hit
    #calc campaigns data
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
    ).order_by('campaign', 'day')
    campaigns = []
    campaign_names = dict(Campaign.objects.all().values_list('id', 'name'))
    for camp, camp_data in itertools.groupby(q, lambda x: x['campaign']):
        current_campaign = {}
        current_campaign['id']=camp
        current_campaign['chart'] = map(calc_another_fields, camp_data)
        summary = reduce(make_sum, current_campaign['chart'])
        summary = calc_another_fields(summary)
        current_campaign.update(summary)
        current_campaign['campaign'] = campaign_names[camp]
        current_campaign.pop('day', None)
        campaigns.append(current_campaign)
    cache.set(key,campaigns)
    return campaigns

one_day = datetime.timedelta(days=1)
def parse_get_params(params):
    res={}
    try:
        res['from_date']= datetime.date.fromtimestamp(int(params["from_date"]))
    except:
        res['from_date']= datetime.date.today() - one_day * 8
    try:
        res['to_date']=datetime.date.fromtimestamp(int(params["to_date"]))
    except:
        res['to_date']=datetime.date.today() - one_day * 1
    try:
        res['advertiser_id']= int(params['advertiser_id'])
    except:
        res['advertiser_id'] = 992089
    try:
        res['skip']= int(params['skip'])
    except:
        res['skip'] = 0
    try:
        res['take']= int(params['take'])
    except:
        res['take'] = 20
    try:
        res['order']= re.match(r"^(desc|asc)$", params['order']).group(1)
    except:
        res['order'] = 'desc'
    try:
        res['sort']= re.match(r"^(campaign|spend|conv|imp|clicks|cpc|cpm|cvr|ctr)$", params['sort']).group(1)
    except:
        res['sort'] = 'campaign'
    try:
        res['stat_by']= re.match(r"^(campaign|spend|conv|imp|clicks|cpc|cpm|cvr|ctr)(?:,(campaign|spend|conv|imp|clicks|cpc|cpm|cvr|ctr))+$",
                                 params['stat_by']).group(0).split(',')
    except:
        res['stat_by'] = ''
    try:
        res['by']= re.match(r"^(campaign|spend|conv|imp|clicks|cpc|cpm|cvr|ctr)(?:,(campaign|spend|conv|imp|clicks|cpc|cpm|cvr|ctr))+$",
                                 params['stat_by']).group(0).split(',')
    except:
        res['by'] = ''
    try:
        res['filter']= [x.split('=')  for x in params['filter'].split(';')]
    except:
        res['filter'] = []

    return res

#http://private-anon-e1f78e3eb-rtbs.apiary-mock.com/api/v1/campaigns?from=from_date&to=to_date&skip=skip&take=take&sort=sort&order=order&stat_by=stat_by&filter=filter
@api_view()
@parser_classes([FormParser, MultiPartParser])
def campaigns(request):
    """
     Get acampaign data for given period
     params:
    """
    print request.query_params
    params = parse_get_params(request.GET)
    result = get_campaigns_data(params['advertiser_id'],params['from_date'],params['to_date'])
    #apply filter
    if params['filter']:
        clause_list = [(i[0],i[1].split(',')) for i in params['filter']]
        def filter_function(camp):
            return all(str(camp[clause[0]])in clause[1] for clause in clause_list)
        result = filter(filter_function,result)

    totalCount = len(result)

    reverse_order = params['order'] == 'desc'
    if params['sort']!='campaign':
        result.sort(key=lambda camp: camp[params['sort']], reverse=reverse_order)
    result=result[params['skip']:params['skip']+params['take']]
    if result:
        if params['stat_by']:
            enabled_fields = set(params['stat_by'])
            # if 'day' not in enabled_fields:
            # enabled_fields.add('day')
            all_fields = set(('conv', 'ctr', 'cpc', 'cvr', 'clicks', 'imp', 'spend', 'cpm'))  # ,'day')
            remove_fields = all_fields - enabled_fields
            for camp in result:
                for point in camp['chart']:
                    for f in remove_fields:
                        point.pop(f, None)
        else:
            for camp in result:
                camp.pop('chart', None)

    #return JsonResponse({"campaigns": result, "totalCount": totalCount})
    return Response({"campaigns": result, "totalCount": totalCount})


def get_days_data(advertiser_id, from_date, to_date):
    key = '_'.join(('rtb_days',str(advertiser_id), from_date.strftime('%Y-%m-%d'),to_date.strftime('%Y-%m-%d'),))
    res = cache.get(key)
    if res:return res
    res = {}
    #no cache hit
    #calc day data
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
    ).order_by('day')
    days = map(calc_another_fields, q)
    summary = reduce(make_sum, days)
    summary = calc_another_fields(summary)
    summary.pop('day', None)
    res['days'] = days
    res['totals'] = summary
    cache.set(key,res)
    return res

#get symmary data for given period
#http://private-anon-e1f78e3eb-rtbs.apiary-mock.com/api/v1/totals?from=from_date&to=to_date
def totals(request):
    params=parse_get_params(request.GET)
    data = get_days_data(params['advertiser_id'],params['from_date'],params['to_date'])
    return JsonResponse({"totals": data['totals']})


#get statistics for period - day by day
#http://private-anon-e1f78e3eb-rtbs.apiary-mock.com/api/v1/statistics?from=from_date&to=to_date&by=by

def statistics(request):
    params=parse_get_params(request.GET)
    data = get_days_data(params['advertiser_id'],params['from_date'],params['to_date'])
    if params['by'] and data:
        entries_to_remove = set(data[0].keys())-set(params['by'])
        for camp in data:
            for f in entries_to_remove:
                camp.pop(f,None)
    return JsonResponse({'statistics':data['days']})

# Get clicks statistics by countries (for period)
#http://private-anon-e1f78e3eb-rtbs.apiary-mock.com/api/v1/map/clicks?from=from_date&to=to_date
def map_clicks(request):
    params=parse_get_params(request.GET)
    return JsonResponse({
        "China": 19,
        "India": 123,
        "United States": 3000,
        "Indonesia": 200,
        "Brazil": 5000,
        "Nigeria": 30000,
        "Bangladesh": 4000,
        "Russia": 1000,
        "Japan": 4,
        "Mexico": 40,
        "Philippines": 600,
        "Germany": 3000,
        "France": 20000,
        "Thailand": 1000,
        "United Kingdom": 200,
        "Italy": 222,
        "Ukraine": 600,
        "Canada": 50
    })

