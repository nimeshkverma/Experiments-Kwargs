from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^social_login/$', views.SocialLogin.as_view(), name='login'),
    url(r'^(?P<pk>[0-9]+)/social_logout/$',
        views.SocialLogout.as_view(), name='logout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
