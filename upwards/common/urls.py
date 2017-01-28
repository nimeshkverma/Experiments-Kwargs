from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^config/$', views.Config.as_view(), name='config'),
    url(r'^college/$', views.CollegeList.as_view()),
    url(r'^college/(?P<pk>[0-9]+)/$', views.CollegeDetail.as_view()),
    url(r'^company/$', views.CompanyList.as_view()),
    url(r'^company/(?P<pk>[0-9]+)/$', views.CompanyDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
