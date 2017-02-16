from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^type/$', views.LoanTypeList.as_view()),
    url(r'^type/(?P<pk>[0-9]+)/$',
        views.LoanTypeDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
