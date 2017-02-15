from __future__ import unicode_literals

from django.db import models

from common.models import InActiveModel, ActiveObjectManager, ActiveModel


class Borrower(InActiveModel):

    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    borrower_type = models.ForeignKey(
        'BorrowerType', on_delete=models.CASCADE, blank=True, null=True)
    credit_limit = models.IntegerField()
    number_of_active_loans = models.IntegerField(default=0)
    number_of_repaid_loans = models.IntegerField(default=0)
    total_current_debt = models.IntegerField(default=0)
    eligible_for_loan = models.BooleanField(
        default=False)
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

# loan_type
# loan_type_id
# type
# one_time_processing_fee
# number_of_repayment_cycles
# accounting_days_in_cycle
# calender_days_in_cycle
# repayment_type
# interest_rate_per_day
# interest_rate_type
# is_processing_fee_deducted_at_source
# is_interest_deducted_at_source
# penalty_amount_per_cycle
# penalty_percent_per_cycle
# created_at
# updated_at
# is_active

INSTALLMENTS = 'installments',
STAGGERED = 'staggered'
REPAYMENT_TYPE_CHOICES = (
    (INSTALLMENTS, 'installments'),
    (STAGGERED, 'staggered'),
)


class LoanType(ActiveModel):
    type_name = models.CharField(
        max_length=100, unique=True)
    one_time_processing_fee = models.DecimalField(
        max_digits=6, decimal_places=4)
    number_of_repayment_cycles = models.IntegerField(default=1)
    accounting_days_in_cycle = models.IntegerField(default=30)
    calender_days_in_cycle = models.IntegerField(default=30)
    repayment_type = models.CharField(
        max_length=50, default=NBFC, choices=REPAYMENT_TYPE_CHOICES)
    max_current_loans_allowed = models.IntegerField(default=1)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "loan_type"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.id), str(self.type_name), str(self.max_current_loans_allowed))


class Lender(ActiveModel):
    name = models.CharField(max_length=100, unique=True)
    lender_type = models.CharField(
        max_length=50, default=NBFC, choices=LENDER_TYPE_CHOICES)
    allocation_limit = models.IntegerField(default=10000000)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "lender"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.id), str(self.name), str(self.lender_type))


# Create your models here.


# loan
# loan_id
# borrower_id
# loan_type_id
# loan_amount_applied
# lender_id
# is_rejected
# rejection_reason
# application_date
# disbursal_date
# created_at
# updated_at
# is_active


# installment
# installment_id
# loan_id
# expected_principal_outstanding
# expected_principal_paid
# expected_interest_paid
# expected_interest_outstanding
# expected_installment_amount
# expected_repayment_date
# actual_principal_outstanding
# actual_principal_paid
# actual_interest_paid
# actual_installment_amount
# actual_repayment_date
# actual_principal_overdue
# actual_interest_overdue
# actual_interest_overdue_cumulative
# actual_total_shortfall
# created_at
# updated_at
# is_active
