import itertools, time, datetime, re
from urllib import addbase

from django.http import JsonResponse
from django.db.models import Avg, Count, Sum
from models import SiteDomainPerformanceReport, Campaign
from django.core.cache import cache

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
        res[k] = dict1.get(k, 0) + dict2.get(k, 0)
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
        res['from_date']= datetime.date.fromtimestamp(int(params["from_date"][0]))
    except:
        res['from_date']= datetime.date.today() - one_day * 8
    try:
        res['to_date']=datetime.date.fromtimestamp(int(params["to_date"][0]))
    except:
        res['to_date']=datetime.date.today() - one_day * 1
    try:
        res['from_date']= params['from_date']
    except:
        res['from_date']=datetime.date.today() - one_day * 8
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
        res['filter']= params['filter'].split(';')
    except:
        res['filter'] = []

    return res
# get campaign data as JSON
#URL:
#http://private-anon-e1f78e3eb-rtbs.apiary-mock.com/api/v1/campaigns?from=from_date&to=to_date&skip=skip&take=take&sort=sort&order=order&stat_by=stat_by&filter=filter
def campaigns(request):
    params = parse_get_params(request.GET)
    result = get_campaigns_data(params['advertiser_id'],params['from_date'],params['to_date'])
    reverse_order = params['order'] == 'desc'
    if params['sort']!='campaign':
        result.sort(key=lambda camp: camp[params['sort']], reverse=reverse_order)
    result=result[params['skip']:params['skip']+params['take']]
    if params['stat_by'] and result:
        entries_to_remove = set(result[0].keys())-set(params['stat_by'])
        for camp in result:
            for f in entries_to_remove:
                camp.pop(f,None)
    return JsonResponse(result, safe=False)

def stats(request):
    # query to db
    # Calc total values for all campaigns
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
    res = list(q)
    total = reduce(make_sum, res)
    result["total"] = calc_another_fields(total)
    result["chart"] = map(calc_another_fields, res)

    # calc data for specific campaigns
    # Apply pagination
    # all_campaigns = list(Campaign.objects.values('id', 'name').order_by('id'))
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id=advertiser_id,
        day__gte=from_date,
        day__lte=to_date,
    ).values_list('campaign_id', flat=True).distinct().order_by('campaign_id')  # .distinct()
    all_campaigns = list(q)
    skip = int(params["skip"][0])
    take = int(params["take"][0])
    all_campaigns = all_campaigns[skip:skip + take]
    if len(all_campaigns) < 1:
        return JsonResponse({"error": "There is no campaigns by this request params"})
    # print all_campaigns
    min_campaign = all_campaigns[0]
    max_campaign = all_campaigns[-1]
    result["campaigns"] = campaigns
    return JsonResponse(result)

