from __future__ import unicode_literals

from django.db import models

from common.models import ActiveObjectManager, ActiveModel

INSTALLMENTS = 'installments',
STAGGERED = 'staggered'
REPAYMENT_TYPE_CHOICES = (
    (INSTALLMENTS, 'installments'),
    (STAGGERED, 'staggered'),
)

SIMPLE = 'simple',
MOMRB = 'momrb'
INTEREST_RATE_TYPE_CHOICES = (
    (SIMPLE, 'Simple'),
    (MOMRB, 'MOMRB'),
)


class Loan(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    loan_type = models.ForeignKey(
        'LoanType', on_delete=models.CASCADE)
    loan_amount_applied = models.DecimalField(max_digits=6, decimal_places=4)
    lender = models.ForeignKey('participant.Lender')
    is_rejected = models.BooleanField(default=True)
    application_datetime = models.DateTimeField(auto_now_add=True)
    disbursal_datetime = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    @staticmethod
    def register_eligibility_result_approved_customer_state(sender, instance, created, **kwargs):
        if created:
            register_customer_state(
                ELIGIBILITY_RESULT_APPROVED_STATE, instance.customer_id)

    class Meta(object):
        db_table = "loan"

    def __unicode__(self):
        return "%s__%s__%s__%s" % (str(self.customer_id), str(self.loan_type), str(self.loan_amount_applied), str(self.application_datetime))


class LoanType(ActiveModel):
    type_name = models.CharField(
        max_length=100, unique=True)
    one_time_processing_fee = models.DecimalField(
        max_digits=6, decimal_places=4)
    number_of_repayment_cycles = models.IntegerField(default=1)
    accounting_days_in_cycle = models.IntegerField(default=30)
    calender_days_in_cycle = models.IntegerField(default=30)
    repayment_type = models.CharField(
        max_length=50, default=INSTALLMENTS, choices=REPAYMENT_TYPE_CHOICES)
    interest_rate_per_day = models.DecimalField(
        max_digits=6, decimal_places=4)
    interest_rate_type = models.CharField(
        max_length=50, default=MOMRB, choices=INTEREST_RATE_TYPE_CHOICES)
    is_processing_fee_deducted_at_source = models.BooleanField(default=True)
    is_interest_deducted_at_source = models.BooleanField(default=False)
    penalty_amount_per_cycle = models.IntegerField(
        default=1, null=True, blank=True)
    penalty_percent_per_cycle = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "loan_type"

    def __unicode__(self):
        return "%s__%s__%s__%s" % (str(self.id), str(self.type_name), str(self.number_of_repayment_cycles), str(self.calender_days_in_cycle))


class Installment(ActiveModel):
    loan = models.ForeignKey(
        'Loan', on_delete=models.CASCADE)
    expected_principal_outstanding = models.DecimalField(
        max_digits=6, decimal_places=4)
    expected_principal_paid = models.DecimalField(
        max_digits=6, decimal_places=4)
    expected_interest_paid = models.DecimalField(
        max_digits=6, decimal_places=4)
    expected_interest_outstanding = models.DecimalField(
        max_digits=6, decimal_places=4)
    expected_installment_amount = models.DecimalField(
        max_digits=6, decimal_places=4)
    expected_repayment_date = models.DateTimeField()
    actual_principal_outstanding = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_principal_paid = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_interest_paid = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_installment_amount = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_repayment_date = models.DateTimeField(null=True, blank=True)
    actual_principal_overdue = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_interest_overdue = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_interest_overdue_cumulative = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    actual_total_shortfall = models.DecimalField(
        max_digits=6, decimal_places=4, null=True, blank=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "installment"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.loan_id))
