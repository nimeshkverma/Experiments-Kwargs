from __future__ import unicode_literals
from django.utils import timezone

from django.db import models
from django.utils.crypto import get_random_string
from common.models import ActiveModel, ActiveObjectManager, mobile_number_regex, numeric_regex
from activity.model_constants import CUSTOMER_STATE_CHOICES, UNKNOWN_STATE

PERSONAL = 'customer_alternate_email'
PROFESSIONAL = 'customer_profession_email'

MESSAGE_TYPE_CHOICES = (
    (PERSONAL, 'customer_alternate_email'),
    (PROFESSIONAL, 'customer_profession_email'),
)


def random_code32():
    return get_random_string(length=32)


def random_number4():
    import random
    return random.randint(1000, 9999)


class EmailVerification(ActiveModel):

    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    email_id = models.EmailField()
    email_type = models.CharField(
        max_length=50, default=PERSONAL, choices=MESSAGE_TYPE_CHOICES)
    verification_code = models.CharField(
        default=random_code32, max_length=32, blank=True)
    is_verified = models.BooleanField(default=False)
    times = models.IntegerField(default=1, blank=True, null=True)

    class Meta(object):
        db_table = "email_verification"

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.email_id), str(self.is_verified))


class Otp(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=12, validators=[
        mobile_number_regex], blank=True, default="")
    otp_code = models.CharField(max_length=12, blank=True)
    times = models.IntegerField(default=1, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    class Meta(object):
        db_table = "otp_verification"

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.email_id), str(self.is_verified))


class PreSignupData(ActiveModel):
    app_registration_id = models.TextField(blank=True, null=False)
    imei = models.CharField(
        validators=[numeric_regex], blank=True, null=False, max_length=16)

    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "pre_signup_data"

    def __unicode__(self):
        return "%s__%s" % (str(self.registration_id), str(self.imei))


class Notification(ActiveModel):
    message_title = models.TextField(blank=True, null=True)
    message_body = models.TextField(blank=True, null=True)
    data_message = models.TextField(blank=True, null=True)
    notification_type = models.CharField(
        choices=CUSTOMER_STATE_CHOICES, default=UNKNOWN_STATE, null=False, max_length=50)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "notification"

    def __unicode__(self):
        return "%s__%s" % (str(self.message_title), str(self.notification_type))
