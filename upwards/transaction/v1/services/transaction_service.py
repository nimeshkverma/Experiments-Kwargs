from transaction.models import Transaction
from loan.models import Loan, Installment
from participant.models import Lender, Borrower
from activity.models import register_customer_state
from activity.model_constants import LOAN_AMOUNT_SUBMIT_STATE


class TransactionUserState(object):

    def __init__(self, transaction_status, transaction_type, status_actor):
        self.__transaction_status = transaction_status
        self.__transaction_type = transaction_type
        self.__status_actor = status_actor
        self.__user_transaction_all_state = {
            'upwards': {
                'loan_avail': {
                    'initiated': LOAN_AMOUNT_SUBMIT_STATE,
                    'processing': None,
                    'completed': None,
                },
                'loan_repay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'interest_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'processing_fee_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'late_fee_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
            },
            'nbfc': {
                'loan_avail': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'loan_repay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'interest_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'processing_fee_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
                'late_fee_pay': {
                    'initiated': None,
                    'processing': None,
                    'completed': None,
                },
            }
        }
        self.user_transaction_state = self.__user_transaction_all_state.get(
            self.__status_actor).get(self.__transaction_type, {}).get(self.__transaction_status, {})

    def set_state(self, customer_id):
        register_customer_state(self.user_transaction_state, customer_id)


class BulletTransaction(object):

    def __init__(self, customer_id, loan_id, lender_id, installment_id):
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

    def update_borrower(self, loan_amount):
        number_of_active_loans = self.borrower_object.number_of_active_loans + 1
        total_current_debt = self.borrower_object.total_current_debt + loan_amount
        number_of_loan_eligibility = number_of_active_loans < self.borrower_object.borrower_type.max_current_loans_allowed
        loan_amount_eligibility = total_current_debt < self.borrower_object.credit_limit
        eligible_for_loan = number_of_loan_eligibility and loan_amount_eligibility
        borrower_data = {
            'number_of_active_loans': number_of_loan_eligibility,
            'total_current_debt': total_current_debt,
            'eligible_for_loan': eligible_for_loan
        }
        Borrower.objects.filter(
            customer_id=self.customer_id).update(**borrower_data)
