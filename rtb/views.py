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
        "from_date" : [to_unix_timestamp(cur_dat - datetime.timedelta(days=8))],
        "to_date": [to_unix_timestamp(cur_dat - datetime.timedelta(days=1))],
        "skip" : "0",
        "take" :"20",
    }
    params.update(request.GET)
    from_date = datetime.date.fromtimestamp(int(params["from_date"][0]))
    to_date = datetime.date.fromtimestamp(int(params["to_date"][0]))

    #query to db
    q = SiteDomainPerformanceReport.objects.values('campaign', 'day').annotate(
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      spend=Sum('post_view_convs'),
      "conv": 8,
      "imp": 5500,
      "clicks": 21,
      "cpc": "$0.31",
      "cpm": "$1.38",
      "cvr": 1,
      "ctr": 2,
    )
    booked_revenue = models.DecimalField(max_digits=35, decimal_places=10)
    clicks = models.IntegerField(null=True, blank=True)
    click_thru_pct = models.FloatField(null=True, blank=True)
    convs_per_mm = models.FloatField(null=True, blank=True)
    convs_rate = models.FloatField(null=True, blank=True)
    cost_ecpa = models.DecimalField(max_digits=35, decimal_places=10)
    cost_ecpc = models.DecimalField(max_digits=35, decimal_places=10)
    cpm = models.DecimalField(max_digits=35, decimal_places=10)
    ctr = models.FloatField(null=True, blank=True)
    imps = models.IntegerField(null=True, blank=True)
    media_cost = models.DecimalField(max_digits=35, decimal_places=10)
    post_click_convs = models.IntegerField(null=True, blank=True)
    post_click_convs_rate = models.FloatField(null=True, blank=True)
    post_view_convs = models.IntegerField(null=True, blank=True)
    post_view_convs_rate = models.FloatField(null=True, blank=True)
    profit = models.DecimalField(max_digits=35, decimal_places=10)
    profit_ecpm = models.DecimalField(max_digits=35, decimal_places=10)
    imps_viewed = models.IntegerField(null=True, blank=True)
    view_measured_imps = models.IntegerField(null=True, blank=True)
    view_rate = models.FloatField(null=True, blank=True)
    view_measurement_rate = models.FloatField(null=True, blank=True)

    print q
    return JsonResponse({"message":"hello, world", "from_date":from_date,"to_date":to_date,})


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
