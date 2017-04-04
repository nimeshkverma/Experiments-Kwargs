from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^loan/type/$', views.LoanTypeList.as_view()),
    url(r'^loan/type/(?P<pk>[0-9]+)/$',
        views.LoanTypeDetail.as_view()),
    url(r'^loan/cost_breakup/$', views.CostBreakupDetails.as_view()),
    url(r'^loan/repayment_schedule/$', views.RepaymentScheduleDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
