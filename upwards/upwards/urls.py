from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from social import views
from customer import views
from common import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^customer/', include('social.urls')),
    url(r'^customer/', include('eligibility.urls')),
    url(r'^customer/', include('customer.urls')),
    url(r'^customer/', include('pan.urls')),
    url(r'^customer/', include('aadhaar.urls')),
    url(r'^customer/', include('common.urls')),
    url(r'^customer/', include('messenger.urls')),
    url(r'^customer/', include('activity.urls')),
    url(r'^common/', include('common.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
