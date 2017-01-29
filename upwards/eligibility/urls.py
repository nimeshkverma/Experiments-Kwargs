from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^finance/$', views.FinanceCreate.as_view(), name='FinanceCreate'),
    url(r'^(?P<pk>[0-9]+)/finance/$',
        views.FinanceDetail.as_view(), name='FinanceDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
