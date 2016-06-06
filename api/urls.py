from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^test/$', views.TestList.as_view()),
    url(r'^test/(?P<pk>[0-9]+)/$', views.TestDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
