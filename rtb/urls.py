from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

from . import views, views_rest, views_adv, views_user
from .controllers import technical_work, video_ad, campaign_create, load_advertiser_data, admin_panel_advertiser
from .ml import ml_video_ad


router = routers.DefaultRouter()
#
# router.register('raw', views.NetworkAnalyticsRawViewSet)
router.register('advertisers', views_rest.AdvertiserViewSet)
router.register('user', views_rest.UsersViewSet)
router.register('appnexus/user', views_rest.AppnexusUsersViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^admin', include(admin.site.urls)),
    url(r'^login', views_user.login_api_new),
    # url(r'^login/', views_auth.obtain_auth_token),
    url(r'^logout', views_user.logout_api),
    url(r'^totals', views.totals),
    url(r'^statistics', views.statistics),
    url(r'^videostatistics[/]?$', video_ad.apiSendVideoCampaignStatistics),
    url(r'^map/clicks', views.map_clicks),
    url(r'^map/imps[/]?$', video_ad.apiSendMapImpsData),
    url(r'^campaigns/(\d+)/cpabuckets', views_adv.bucketsCPA),
    url(r'^campaigns/(\d+)/graphinfo', views_adv.graphInfo),
    url(r'^videocampaigns/(\d+)/graphinfo[/]?$', video_ad.apiSendCampaignPageGraph),
    url(r'^videocampaigns/(\d+)/mlgraph[/]?$', ml_video_ad.apiSendMLGraphInfo),
    url(r'^videocampaigns/(\d+)/mlsetalgo[/]?$', ml_video_ad.apiSetCampaignAlgo),
    url(r'^campaigns/(\d+)/cpareport', views_adv.cpaReport),
    url(r'^campaigns/(\d+)/domains', views_adv.campaignDomains),
    url(r'^campaigns/(\d+)/details', views_adv.campaignDetails),
    url(r'^campaigns/(\d+)/MLPlacement', views_adv.mlApiAnalitics),
    url(r'^campaigns/(\d+)/rules', views_adv.ApiCampaignRules),
    url(r'^campaign/create/bulk[/]?$', campaign_create.campaignCreateBulk),
    url(r'^MLRandomTestSet', views_adv.mlApiRandomTestSet),
    url(r'^MLExpertMark', views_adv.mlApiSaveExpertPlacementMark),
    url(r'^MLGetAUC', views_adv.mlApiCalcAUC),
    url(r'^campaigns/(\d+)/changestate', views_adv.changeState),
    url(r'^campaigns/(\d+)$', views_adv.singleCampaign),
    url(r'^campaigns', views.campaigns),
    url(r'^advertiser/campaign/all[/]?$', views_adv.advertisercampaigns),
    url(r'^advertiser/(\d+)[/]?$', views_adv.advertiserSingle),
    url(r'^advertiser/(\d+)/update[/]?$', load_advertiser_data.loadAdvertiserData),
    url(r'^videocampaigns[/]?$', video_ad.apiSendVideoCampaignData),
    url(r'^technicalwork/last[/]?$', technical_work.getLast),
    url(r'^technicalwork[/]?$', technical_work.handler),
    url(r'^advertisersType[/]?$', admin_panel_advertiser.apiSetAdType),
    url(r'^advertisersDataSource[/]?$', admin_panel_advertiser.apiSetAdDataSource),
    url(r'^advertisersRulesType[/]?$', admin_panel_advertiser.apiSetAdRulesType),
    url(r'^banner[/]?$', technical_work.banner)
]
