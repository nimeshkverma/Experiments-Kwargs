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
    url(r'^common/', include('common.urls')),

]
