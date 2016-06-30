from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
                  url(r'^api/v1/', include('rtb.urls')),
                  url(r'^docs/', include('rest_framework_docs.urls')),
                  url(r'^$', RedirectView.as_view(url='/client/index.html'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

