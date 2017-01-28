from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^personal/$', views.CustomerList.as_view(),
        name='customer_personal_data_list'),
    url(r'^(?P<pk>[0-9]+)/personal/$',
        views.CustomerDetail.as_view(), name='customer_personal_data_details'),
    url(r'^bank/$', views.BankDetailsList.as_view(),
        name='customer_bank_data_list'),
    url(r'^(?P<pk>[0-9]+)/bank/$',
        views.BankDetails.as_view(), name='customer_bank_data_details'),
]
