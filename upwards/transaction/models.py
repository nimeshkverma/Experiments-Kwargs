from __future__ import unicode_literals

from django.db import models

from common.models import ActiveObjectManager, ActiveModel


INITIATED = 'initiated'
PROCESSING = 'processing'
COMPLETED = 'completed'

TRANSACTION_STATUS_CHOICES = (
    (INITIATED, 'Initiated'),
    (PROCESSING, 'Processing'),
    (COMPLETED, 'Completed'),
)

LOAN_AVAIL = 'loan_avail'
LOAN_REPAY = 'loan_repay'
INTEREST_PAY = 'interest_pay'
PROCESSING_FEE_PAY = 'processing_fee_pay'
LATE_FEE_PAY = 'late_fee_pay'

TRANSACTION_TYPE_CHOICES = (
    (LOAN_AVAIL, 'Loan Avail'),
    (LOAN_REPAY, 'Loan Repay'),
    (INTEREST_PAY, 'Interest Pay'),
    (PROCESSING_FEE_PAY, 'Processing Fee Pay'),
    (LATE_FEE_PAY, 'Late Fee Pay'),
)

NBFC = 'nbfc'
UPWARDS = 'upwards'

STATUS_ACTOR_CHOICES = (
    (NBFC, 'NBFC'),
    (UPWARDS, 'Upwards'),
)


class Transaction(ActiveModel):
    customer = models.ForeignKey(
        'participant.Borrower', to_field="customer", on_delete=models.CASCADE)
    loan = models.ForeignKey('loan.Loan', on_delete=models.CASCADE)
    installment = models.ForeignKey(
        'loan.Installment', on_delete=models.CASCADE)
    lender = models.ForeignKey(
        'participant.Lender', on_delete=models.CASCADE)
    utr = models.CharField(max_length=50, null=True, blank=True)
    transaction_status = models.CharField(
        max_length=50, default=INITIATED, choices=TRANSACTION_STATUS_CHOICES)
    transaction_type = models.CharField(
        max_length=50, default=LOAN_AVAIL, choices=TRANSACTION_TYPE_CHOICES)
    status_actor = models.CharField(
        max_length=50, default=UPWARDS, choices=STATUS_ACTOR_CHOICES)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "transaction"

    def __unicode__(self):
        return "%s__%s__%s__%s" % (str(self.customer_id), str(self.loan_id), str(self.installment_id), str(self.utr))
