from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from common.models import (LifeTimeTrackingModel,
                           alphabet_whitespace_regex_allow_empty,
                           GENDER_CHOICES,
                           MALE)

FACEBOOK = 'facebook'
GOOGLE = 'google'
PLATFORM_CHOICES = (
    (FACEBOOK, 'Facebook'),
    (GOOGLE, 'Google Plus'),
)

WEB = 'web'
ANDROID = 'android'
IOS = 'ios'
SOURCE_CHOICES = (
    (WEB, 'Web'),
    (ANDROID, 'Android'),
    (IOS, 'IOS'),
)


class Login(LifeTimeTrackingModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    email_id = models.EmailField()
    platform = models.CharField(
        max_length=20, default=GOOGLE, choices=PLATFORM_CHOICES)
    source = models.CharField(
        max_length=20, default=ANDROID, choices=SOURCE_CHOICES)
    social_data = models.TextField(editable=False, blank=True, null=False)
    platform_token = models.TextField(editable=False, blank=True, null=False)
    session_token = models.CharField(
        editable=False, blank=True, null=True, max_length=64)

    @staticmethod
    def email_related_logins(email_id):
        return Login.objects.filter(email_id=email_id)

    @staticmethod
    def customer_and_session_login(session_token, customer_id):
        return Login.objects.filter(session_token=session_token, customer_id=customer_id, is_active=True).order_by('-updated_at').first()

    @staticmethod
    def delete_session(session_token, customer_id):
        Login.objects.filter(session_token=session_token, customer_id=customer_id, is_active=True).update(
            session_token=None, is_active=False, deleted_at=timezone.now())

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.email_id), str(self.platform))


# class Profile(LifeTimeTrackingModel):
#     customer = models.ForeignKey('Login', on_delete=models.CASCADE)
#     email_id = models.EmailField(blank=False, null=False)
#     platform_id = models.CharField(max_length=256, blank=False, null=False)
#     platform = models.CharField(
#         max_length=20, default=GOOGLE, choices=PLATFORM_CHOICES)
#     first_name = models.CharField(max_length=25, validators=[
#         alphabet_whitespace_regex_allow_empty], default="")
#     last_name = models.CharField(max_length=25, validators=[
#         alphabet_whitespace_regex_allow_empty], default="")
#     gender = models.CharField(
#         max_length=1, default=MALE, choices=GENDER_CHOICES)
#     profile_link = models.URLField()
#     profile_pic_link = models.URLField()

#     def __unicode__(self):
# return "%s__%s__%s" % (str(self.customer), str(self.email_id),
# str(self.platform))


# class LinkedinProfile(LifeTimeTrackingModel):
#     customer = models.ForeignKey('Login', on_delete=models.CASCADE)
#     email_id = models.EmailField(blank=False, null=False)
#     linkedin_id = models.CharField(max_length=256, blank=False, null=False)
#     first_name = models.CharField(max_length=25, validators=[
#         alphabet_whitespace_regex_allow_empty], default="")
#     last_name = models.CharField(max_length=25, validators=[
#         alphabet_whitespace_regex_allow_empty], default="")
#     gender = models.CharField(
#         max_length=1, default=MALE, choices=GENDER_CHOICES)
#     profile_link = models.URLField()
#     profile_pic_link = models.URLField()
#     industry = models.CharField(max_length=100, default="")
#     location = models.CharField(max_length=100, default="")
#     last_employer = models.CharField(max_length=100, default="")
#     join_date_last_employer = models.DateField(blank=False, null=False)
#     connections = models.   IntegerField(default=500)

#     class Meta(object):
#         db_table = "customer_linkedin_profile"

#     def __unicode__(self):
# return "%s__%s__%s" % (str(self.customer), str(self.email_id),
# str(self.platform))
