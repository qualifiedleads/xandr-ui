from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.views import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/client/', include('domain_api.urls')),
    url(r'^api/v1/', include('rtb.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^$', RedirectView.as_view(url='/client/dist/index.html'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

