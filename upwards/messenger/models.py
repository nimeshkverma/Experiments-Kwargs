from __future__ import unicode_literals
from django.utils import timezone

from django.db import models
from django.utils.crypto import get_random_string
from common.models import (ActiveModel,
                           UpdateSignalManager,
                           post_update)

PERSONAL = 'customer_altername_email'
PROFESSIONAL = 'customer_profession_email'

MESSAGE_TYPE_CHOICES = (
    (PERSONAL, 'customer_altername_email'),
    (PROFESSIONAL, 'customer_profession_email'),
)


def random_code32():
    return get_random_string(length=32)


class EmailVerification(ActiveModel):

    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    email_id = models.EmailField()
    email_type = models.CharField(
        max_length=50, default=PERSONAL, choices=MESSAGE_TYPE_CHOICES)
    verification_code = models.CharField(
        default=random_code32, max_length=32, blank=True)
    is_verified = models.BooleanField(default=False)
    objects = UpdateSignalManager()

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.email_id), str(self.is_verified))


def update_others(sender, instance, created, **kwargs):
    instance.customer.is_altername_email_id_verified = True
    instance.customer.save()

post_update.connect(update_others, sender=EmailVerification)
