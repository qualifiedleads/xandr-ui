from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register('raw', views.NetworkAnalyticsRawViewSet)

urlpatterns = [
                  url(r'^', include(router.urls)),
                  url(r'^admin/', include(admin.site.urls)),
              ]
