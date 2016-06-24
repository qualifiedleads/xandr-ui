from django.contrib.admin.templatetags.admin_list import result_headers
from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse
from django.db.models import Avg, Count, Sum
import time
import datetime

from .models import NetworkAnalyticsRaw, User, SiteDomainPerformanceReport, Campaign

def to_unix_timestamp(d):
    return str(int(time.mktime(d.timetuple())))

def calc_another_fields(obj):
    res = {}
    res.update(obj)
    res['conv'] = (obj.get('conv',0) or 0) + (obj.get('conv_click',0) or 0) + (obj.get('conv_view',0) or 0)
    res['cpc'] = obj['spend'] / obj['clicks'] if obj['clicks'] else 0
    res['cpm'] = obj["spend"] / obj['imp'] * 1000 if obj['imp'] else 0
    res['cvr'] = res["conv"] / obj['imp']  if obj['imp'] else 0
    res['cvr'] = obj["clicks"] / obj['imp']  if obj['imp'] else 0
    res.pop('conv_click',None)
    res.pop('conv_view',None)

    return res

def make_sum(dict1,dict2):
    res = {}
    for k in dict1:
        res[k] = dict1.get(k,0)+dict2.get(k,0)
    return res

def stats(request):
    cur_dat = datetime.date.today()
    #from_date = request.GET.get('from_date', cur_dat - datetime.timedelta(days=8))
    #to_date = request.GET.get('to_date', cur_dat - datetime.timedelta(days=1))
    result={}
    params = {
        "advertiser_id": "992089",
        "from_date" : [to_unix_timestamp(cur_dat - datetime.timedelta(days=8))],
        "to_date": [to_unix_timestamp(cur_dat - datetime.timedelta(days=1))],
        "skip" : ["0"],
        "take" :["20"],
    }
    params.update(request.GET)
    from_date = datetime.date.fromtimestamp(int(params["from_date"][0]))
    to_date = datetime.date.fromtimestamp(int(params["to_date"][0]))
    advertiser_id = int(params["advertiser_id"])
    #query to db
    #Calc total values for all campaigns
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id = advertiser_id,
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
    result["chart"]= map(calc_another_fields, res)

    #calc data for specific campaigns
    #Apply pagination
    #all_campaigns = list(Campaign.objects.values('id', 'name').order_by('id'))
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id=advertiser_id,
        day__gte=from_date,
        day__lte=to_date,
    ).values_list('campaign_id',flat=True).distinct().order_by('campaign_id') #.distinct()
    all_campaigns = list(q)
    skip = int(params["skip"][0])
    take = int(params["take"][0])
    all_campaigns = all_campaigns[skip:skip+take]
    if len(all_campaigns)<1:
        return JsonResponse({"error":"There is no campaigns by this request params"})
    #print all_campaigns
    min_campaign = all_campaigns[0]
    max_campaign = all_campaigns[-1]
    q = SiteDomainPerformanceReport.objects.filter(
        advertiser_id = advertiser_id,
        day__gte=from_date,
        day__lte=to_date,
        campaign_id__gte=min_campaign,
        campaign_id__lte=max_campaign,
    ).values('campaign', 'day').annotate(
        #spend=Sum('booked_revenue'),
        spend=Sum('media_cost'),
        #conv=Sum('convs_per_mm'),
        conv_click =Sum('post_click_convs'),
        conv_view =Sum('post_view_convs'),
        #conv=Sum('post_click_convs') + Sum('post_view_convs'),
        imp=Sum('imps'),
        clicks=Sum('clicks'),
        #cpc=Sum('media_cost')/Sum('clicks'), #Cost per click
        ###cpc=Avg('cost_ecpc'),
        #cpm=Sum('media_cost')/Sum('imps')*1000, #Cost per view
        #cvr=(Sum('post_click_convs') + Sum('post_view_convs'))/Sum('imps'),
        #ctr=Sum('clicks') / Sum('imps'),
    ).order_by('campaign', 'day')
    campaign_data = list(q)
    campaign_names = {x[0]:x[1] for x in Campaign.objects.filter(id__in=all_campaigns).values_list('id','name')}
    for camp in campaign_data:
        camp['campaign']=campaign_names[camp['campaign']]
    result["campaigns"] = campaign_data
    return JsonResponse(result)


class NetworkAnalyticsRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkAnalyticsRaw
        fields = ()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class NetworkAnalyticsRawViewSet(viewsets.ModelViewSet):
    queryset = NetworkAnalyticsRaw.objects.all()

    serializer_class = NetworkAnalyticsRawSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_class = UsersSerializer
