from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^algo360/$', views.Algo360DataDetails.as_view(),
        name='Algo360DataDetails'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
