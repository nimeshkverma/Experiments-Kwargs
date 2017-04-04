from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^customer/pan/$', views.PanCreate.as_view(), name='PanCreate'),
    url(r'^customer/(?P<pk>[0-9]+)/pan/$',
        views.PanDetail.as_view(), name='PanDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
