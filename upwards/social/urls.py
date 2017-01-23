from django.conf.urls import url
from social import views

urlpatterns = [
    url(r'^customer/$', views.CustomerList.as_view()),
    url(r'^customer/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view()),
    url(r'^login/$', views.LoginList.as_view()),
    url(r'^login/(?P<pk>[0-9]+)/$', views.LoginDetail.as_view()),
    url(r'^social_login/$', views.SocialLogin.as_view()),
]
