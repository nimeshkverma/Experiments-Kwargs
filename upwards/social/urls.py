from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.SocialLogin.as_view(), name='login'),
    url(r'^logout/$', views.SocialLogout.as_view(), name='logout'),
]
