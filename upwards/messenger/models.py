from __future__ import unicode_literals
from django.utils import timezone

from django.db import models
from django.utils.crypto import get_random_string
from common.models import ActiveModel, mobile_number_regex

PERSONAL = 'customer_altername_email'
PROFESSIONAL = 'customer_profession_email'

MESSAGE_TYPE_CHOICES = (
    (PERSONAL, 'customer_altername_email'),
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
