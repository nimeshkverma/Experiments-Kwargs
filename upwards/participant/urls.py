from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^borrower/$', views.BorrowerCreate.as_view(),
        name='BorrowerCreate'),
    url(r'^borrower/(?P<pk>[0-9]+)/$',
        views.BorrowerDetail.as_view(), name='BorrowerDetail'),
    url(r'^borrower_type/$', views.BorrowerTypeList.as_view()),
    url(r'^borrower_type/(?P<pk>[0-9]+)/$',
        views.BorrowerTypeDetail.as_view()),
    url(r'^lender/$', views.LenderList.as_view()),
    url(r'^lender/(?P<pk>[0-9]+)/$',
        views.LenderDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
