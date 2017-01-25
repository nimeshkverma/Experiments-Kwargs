from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^config/$', views.Config.as_view(), name='config'),
]
