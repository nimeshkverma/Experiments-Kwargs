from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^transaction/loan_request/$',
        views.LoanRequestTransactionDetails.as_view()),
    url(r'^transaction/timeline/$', views.TransactionHistoryDetails.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
