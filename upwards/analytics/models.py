from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import post_save
from activity.models import register_activity, register_customer_state
from activity.model_constants import PAN_SUBMIT_STATE, CUSTOMER, PAN_SUBMIT

from common.models import (ActiveModel,
                           ActiveObjectManager,
                           numeric_regex,)


class Algo360(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    imei = models.CharField(
        validators=[numeric_regex], editable=False, blank=True, null=False, max_length=16)
    monthly_average_balance_lifetime = models.CharField(
        max_length=100, blank=True, null=False)
    monthly_average_balance_12 = models.CharField(
        max_length=100, blank=True, null=False)
    monthly_average_balance_6 = models.CharField(
        max_length=100, blank=True, null=False)
    monthly_average_balance_3 = models.CharField(
        max_length=100, blank=True, null=False)
    monthly_average_balance_1 = models.CharField(
        max_length=100, blank=True, null=False)
    number_of_cheque_bounce_1 = models.CharField(
        max_length=100, blank=True, null=False)
    number_of_cheque_bounce_3 = models.CharField(
        max_length=100, blank=True, null=False)
    is_credit_card_overlimited = models.CharField(max_length=100, default=True)
    credit_card_last_payment_due = models.CharField(
        max_length=100, blank=True, null=False)
    salary = models.CharField(max_length=100, blank=True, null=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "analytics_algo360"
