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
    url(r'^amount_eligible/$', views.AmountEligibleCreate.as_view(),
        name='AmountEligibleCreate'),
    url(r'^(?P<pk>[0-9]+)/amount_eligible/$',
        views.AmountEligibleDetail.as_view(), name='AmountEligibleDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
