from transaction.models import Transaction
from loan.models import Loan, Installment
from participant.models import Lender, Borrower


class BulletTransaction(object):

    def __init__(self, customer_id, loan_id, lender_id, installment_id):
        print 'customer_id, loan_id, lender_id, installment_id', customer_id, loan_id, lender_id, installment_id
        self.customer_id = customer_id
        self.borrower_object = Borrower.objects.get(
            customer_id=self.customer_id)
        self.loan_id = loan_id
        self.loan_object = Loan.objects.get(pk=self.loan_id)
        self.lender_id = lender_id
        self.lender_object = Lender.objects.get(pk=self.lender_id)
        self.installment_id = installment_id
        self.installment_object = Installment.objects.get(
            pk=self.installment_id)

    def create_loan_request_transaction(self, transaction_status, transaction_type, status_actor, utr=None):
        transaction_data = {
            'customer': self.borrower_object,
            'loan': self.loan_object,
            'lender': self.lender_object,
            'installment': self.installment_object,
            'utr': utr,
            'transaction_status': transaction_status,
            'transaction_type': transaction_type,
            'status_actor': status_actor
        }
        return Transaction.objects.create(**transaction_data)
