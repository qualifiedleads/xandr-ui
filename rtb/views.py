from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets
from django.http import JsonResponse
from django.db.models import Avg, Count, Sum
import time
import datetime

from .models import NetworkAnalyticsRaw, User, SiteDomainPerformanceReport

def to_unix_timestamp(d):
    return str(int(time.mktime(d.timetuple())))

def stats(request):
    cur_dat = datetime.date.today()
    #from_date = request.GET.get('from_date', cur_dat - datetime.timedelta(days=8))
    #to_date = request.GET.get('to_date', cur_dat - datetime.timedelta(days=1))

    params = {
        "advertiser_id": "992089",
        "from_date" : [to_unix_timestamp(cur_dat - datetime.timedelta(days=8))],
        "to_date": [to_unix_timestamp(cur_dat - datetime.timedelta(days=1))],
        "skip" : "0",
        "take" :"20",
    }
    params.update(request.GET)
    from_date = datetime.date.fromtimestamp(int(params["from_date"][0]))
    to_date = datetime.date.fromtimestamp(int(params["to_date"][0]))
    advertiser_id = int(params["advertiser_id"])
    #query to db
    q = SiteDomainPerformanceReport.objects.filter(advertiser_id = advertiser_id).values('campaign', 'day').annotate(
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
    ).order_by('campaign', 'day')#.order_by('day')
    r = list(q)
    print r
    return JsonResponse({"message":r, "from_date":from_date,"to_date":to_date,})


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
