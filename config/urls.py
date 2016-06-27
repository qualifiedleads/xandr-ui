from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
urlpatterns = [
                  url(r'^api/v1/', include('rtb.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
