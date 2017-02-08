from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/state_change/$',
        views.CustomerStateChange.as_view(), name='CustomerStateChange'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
