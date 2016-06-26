import itertools, time, datetime
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
    res['cvr'] = obj["clicks"] / obj['imp'] if obj['imp'] else 0
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
    key = '_'.join('rtb_campaigns',(advertiser_id, from_date.strftime('%Y-%m-%d'),to_date.strftime('%Y-%m-%d'),))
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

def stats(request):
    cur_dat = datetime.date.today()
    # from_date = request.GET.get('from_date', cur_dat - datetime.timedelta(days=8))
    # to_date = request.GET.get('to_date', cur_dat - datetime.timedelta(days=1))
    result = {}
    params = {
        "advertiser_id": "992089",
        "from_date": [to_unix_timestamp(cur_dat - datetime.timedelta(days=8))],
        "to_date": [to_unix_timestamp(cur_dat - datetime.timedelta(days=1))],
        "skip": ["0"],
        "take": ["20"],
    }
    params.update(request.GET)
    from_date = datetime.date.fromtimestamp(int(params["from_date"][0]))
    to_date = datetime.date.fromtimestamp(int(params["to_date"][0]))
    advertiser_id = int(params["advertiser_id"])
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

