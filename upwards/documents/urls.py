from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^document/$', views.DocumentsCreate.as_view(), name='DocumentsCreate'),
    url(r'^(?P<pk>[0-9]+)/document/$',
        views.DocumentsDetail.as_view(), name='DocumentsDetail'),
    url(r'^document_type/$', views.DocumentTypeList.as_view()),
    url(r'^(?P<pk>[0-9]+)/document_type/$',
        views.DocumentTypeDetail.as_view()),
    url(r'^(?P<pk>[0-9]+)/documents_uploaded/$',
        views.DocumentsUploadDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
