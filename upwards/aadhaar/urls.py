from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^aadhaar/$', views.AadhaarCreate.as_view(), name='AadhaarCreate'),
    url(r'^(?P<pk>[0-9]+)/aadhaar/$',
        views.AadhaarDetail.as_view(), name='AadhaarDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
