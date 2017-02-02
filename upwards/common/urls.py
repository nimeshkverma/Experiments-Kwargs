from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^config/$', views.Config.as_view(), name='config'),
    url(r'^college/$', views.CollegeList.as_view()),
    url(r'^college/(?P<pk>[0-9]+)/$', views.CollegeDetail.as_view()),
    url(r'^company/$', views.CompanyList.as_view()),
    url(r'^company/(?P<pk>[0-9]+)/$', views.CompanyDetail.as_view()),
    url(r'^salary_payment_mode/$', views.SalaryPaymentModeList.as_view()),
    url(r'^salary_payment_mode/(?P<pk>[0-9]+)/$',
        views.SalaryPaymentModeDetail.as_view()),
    url(r'^organisation_type/$', views.OrganisationTypeList.as_view()),
    url(r'^organisation_type/(?P<pk>[0-9]+)/$',
        views.OrganisationTypeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
