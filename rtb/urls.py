from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

from . import views, views_rest, views_adv

router = routers.DefaultRouter()
#
# router.register('raw', views.NetworkAnalyticsRawViewSet)
router.register('advertisers', views_rest.AdvertiserViewSet)
router.register('user', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin', include(admin.site.urls)),
    url(r'^totals', views.totals),
    url(r'^statistics', views.statistics),
    url(r'^map/clicks', views.map_clicks),
    url(r'^campaigns/(\d+)/graphinfo', views_adv.graphInfo),
    url(r'^campaigns/(\d+)/cpareport', views_adv.cpaReport),
    url(r'^campaigns/(\d+)/domains', views_adv.campaignDomains),
    url(r'^campaigns/(\d+)/details', views_adv.campaignDetails),
    url(r'^campaigns/(\d+)$', views_adv.singleCampaign),
    url(r'^campaigns', views.campaigns),
]
