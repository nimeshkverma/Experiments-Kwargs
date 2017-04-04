from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^customer/send_verification_email/$', views.EmailVerificationCreate.as_view(),
        name='send_verification_email'),
    url(r'^customer/verify_email/(?P<encoded_data>[\w:_-]+)$',
        views.EmailVerificationDetail.as_view(), name='verify_email'),
    url(r'^customer/send_otp/$', views.OtpCreate.as_view(),
        name='send_otp'),
    url(r'^customer/pre_signup_data/$', views.PreSignupDataDetails.as_view(),
        name='PreSignupDataDetails'),
    url(r'^customer/notification/$', views.NotificationDetails.as_view(),
        name='NotificationDetails'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
