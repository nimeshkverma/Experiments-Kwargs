from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^finance/$', views.FinanceCreate.as_view(), name='FinanceCreate'),
    url(r'^(?P<pk>[0-9]+)/finance/$',
        views.FinanceDetail.as_view(), name='FinanceDetail'),
    url(r'^profession/$', views.ProfessionCreate.as_view(), name='ProfessionCreate'),
    url(r'^(?P<pk>[0-9]+)/profession/$',
        views.ProfessionDetail.as_view(), name='ProfessionDetail'),
    url(r'^education/$', views.EducationCreate.as_view(), name='EducationCreate'),
    url(r'^(?P<pk>[0-9]+)/education/$',
        views.EducationDetail.as_view(), name='EducationDetail'),
    url(r'^vahan_data/$',
        views.VahanDataDetail.as_view(), name='VahanDataDetail'),
    url(r'^vahan/$', views.VahanCreate.as_view(), name='VahanCreate'),
    url(r'^(?P<pk>[0-9]+)/vahan/$',
        views.VahanDetail.as_view(), name='VahanDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
