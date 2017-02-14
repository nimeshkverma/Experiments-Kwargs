from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save

from common.models import InActiveModel, ActiveObjectManager, ActiveModel
from activity.models import register_customer_state
from activity.model_constants import ELIGIBILITY_RESULT_APPROVED_STATE


class Borrower(InActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    borrower_type = models.ForeignKey(
        'BorrowerType', on_delete=models.CASCADE, blank=True, null=True)
    credit_limit = models.IntegerField()
    number_of_active_loans = models.IntegerField(default=0)
    number_of_repaid_loans = models.IntegerField(default=0)
    total_current_debt = models.IntegerField(default=0)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    @staticmethod
    def register_eligibility_result_approved_customer_state(sender, instance, created, **kwargs):
        if created:
            register_customer_state(
                ELIGIBILITY_RESULT_APPROVED_STATE, instance.customer_id)

    class Meta(object):
        db_table = "borrower"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer_id), str(self.credit_limit), str(self.total_current_debt))

post_save.connect(
    Borrower.register_eligibility_result_approved_customer_state, sender=Borrower)


class BorrowerType(ActiveModel):
    type_name = models.CharField(
        max_length=100, unique=True)
    max_current_loans_allowed = models.IntegerField(default=1)


class Lender(ActiveModel):
    name = models.CharField(max_length=100, unique=True)


# lender_id
# name
# type
# allocation_limit
# created_at
# updated_at
# is_active
# borrower_type
# borrower_type_id
