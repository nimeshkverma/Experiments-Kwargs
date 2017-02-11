from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^social_login/$', views.SocialLogin.as_view(), name='SocialLogin'),
    url(r'^(?P<pk>[0-9]+)/social_logout/$',
        views.SocialLogout.as_view(), name='SocialLogout'),
    url(r'^linkedin_auth/$',
        views.LinkedinAuth.as_view(), name='LinkedinAuth'),
    url(r'^(?P<customer_id>[0-9]+)/social_profile/$',
        views.CustomerProfile.as_view(), name='CustomerProfile')

]

urlpatterns = format_suffix_patterns(urlpatterns)
