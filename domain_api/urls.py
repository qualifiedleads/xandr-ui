from django.conf.urls import url
from views import DomainListView, DetailDomainListView, applyDomainList, CampaignListView

urlpatterns = [
    url(r'^$', DomainListView.as_view(), name='domain_list'),  # get / post
    url(r'^campaign[/]?$', CampaignListView.as_view(), name='campaign_list'),  # get / post
    url(r'^(?P<pk>[0-9]+)[/]?$', DetailDomainListView.as_view(), name='datail_domain_list'),  # get / put / delete
    url(r'^(?P<pk>[0-9]+)/apply[/]?$', applyDomainList),  # get
]
