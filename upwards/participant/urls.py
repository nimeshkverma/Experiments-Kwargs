from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^borrower/$', views.BorrowerCreate.as_view(),
        name='BorrowerCreate'),
    url(r'^borrower/(?P<pk>[0-9]+)/$',
        views.BorrowerDetail.as_view(), name='BorrowerDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
