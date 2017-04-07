from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^third_party_leads/(?P<third_party>[\w\-]+)/borrower/$',
        views.ThirdPartyLeadList.as_view()),
    url(r'^third_party_leads/(?P<third_party>[\w\-]+)/borrower/(?P<pk>[0-9]+)/$',
        views.ThirdPartyLeadDetail.as_view()),
    url(r'^third_party_leads/(?P<third_party>[\w\-]+)/borrower/document/$',
        views.ThirdPartyLeadDocumentsCreate.as_view(), name='ThirdPartyLeadDocumentsCreate'),
    url(r'^third_party_leads/(?P<third_party>[\w\-]+)/borrower/(?P<pk>[0-9]+)/document/$',
        views.ThirdPartyLeadDocumentsDetail.as_view(), name='ThirdPartyLeadDocumentsDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
