from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^customer/finance/$', views.FinanceCreate.as_view(), name='FinanceCreate'),
    url(r'^customer/(?P<pk>[0-9]+)/finance/$',
        views.FinanceDetail.as_view(), name='FinanceDetail'),
    url(r'^customer/profession/$',
        views.ProfessionCreate.as_view(), name='ProfessionCreate'),
    url(r'^customer/(?P<pk>[0-9]+)/profession/$',
        views.ProfessionDetail.as_view(), name='ProfessionDetail'),
    url(r'^customer/education/$',
        views.EducationCreate.as_view(), name='EducationCreate'),
    url(r'^customer/(?P<pk>[0-9]+)/education/$',
        views.EducationDetail.as_view(), name='EducationDetail'),
    url(r'^customer/vahan_data/$',
        views.VahanDataDetail.as_view(), name='VahanDataDetail'),
    url(r'^customer/vahan/$', views.VahanCreate.as_view(), name='VahanCreate'),
    url(r'^customer/(?P<pk>[0-9]+)/vahan/$',
        views.VahanDetail.as_view(), name='VahanDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
