import datetime
import decimal
from loan import models
from common.utils import math_utils

# application_date = serializers.DateField()


class BulletLoan(object):

    def __init__(self, loan_amount_asked, loan_type_id):
        self.loan_amount_asked = decimal.Decimal(loan_amount_asked)
        self.loan_type_id = loan_type_id
        self.loan_type_object = self.__get_loan_type_object()

    def __get_loan_type_object(self):
        loan_type_object = None
        loan_type_objects = models.LoanType.objects.filter(
            id=self.loan_type_id)
        if len(loan_type_objects) == 1:
            loan_type_object = loan_type_objects[0]
        return loan_type_object

    def __loan_principal(self):
        loan_principal_data = {
            "field_name": "Loan Principal (Rs)",
            "field_value": str(self.loan_amount_asked),
        }
        return loan_principal_data

    def __get_one_time_processing_fee(self):
        one_time_processing_fee = decimal.Decimal(0)
        if self.loan_type_object.is_processing_fee_deducted_at_source:
            one_time_processing_fee = self.loan_type_object.one_time_processing_fee
        return one_time_processing_fee

    def __processing_fee_field_name(self):
        processing_fee_field_name = "Processing fee @ {interest}% (Rs)"
        return processing_fee_field_name.format(interest=str(self.__get_one_time_processing_fee()))

    def __processing_fee_field_value(self):
        print decimal.Decimal(-1.0) * math_utils.positive_ceil(self.__get_one_time_processing_fee() * self.loan_amount_asked, 2), 1
        return decimal.Decimal(-0.01) * math_utils.positive_ceil(self.__get_one_time_processing_fee() * self.loan_amount_asked, 2)

    def __processing_fee(self):
        processing_fee_data = {
            "field_name": self.__processing_fee_field_name(),
            "field_value": str(self.__processing_fee_field_value()),
        }
        return processing_fee_data

    def _get_interest_fee(self):
        interest_fee = 0
        if self.loan_type_object.is_interest_deducted_at_source:
            interest_fee = math_utils.positive_ceil(
                self.loan_type_object.interest_rate_per_day * self.loan_type_object.accounting_days_in_cycle, 0)
        return decimal.Decimal(interest_fee)

    def __interest_fee_field_name(self):
        interest_fee_field_name = "Interest fee @ {interest}% (Rs)"
        return interest_fee_field_name.format(interest=self._get_interest_fee())

    def __interest_fee_field_value(self):
        print self._get_interest_fee() * self.loan_amount_asked, 9
        return decimal.Decimal(-0.01) * math_utils.positive_ceil(self._get_interest_fee() * self.loan_amount_asked, 2)

    def __interest_fee(self):
        interest_fee_data = {
            "field_name": self.__interest_fee_field_name(),
            "field_value": str(self.__interest_fee_field_value()),
        }
        return interest_fee_data

    def __net_amount_credited_field_value(self):
        net_amount_credited = self.loan_amount_asked + \
            self.__interest_fee_field_value() + self.__processing_fee_field_value()
        return math_utils.positive_ceil(net_amount_credited, 2)

    def __net_amount_credited(self):
        net_amount_credited = {
            "field_name": "Net amount credited (Rs)",
            "field_value": str(self.__net_amount_credited_field_value()),
        }
        return net_amount_credited

    def cost_breakup_data(self):
        return [
            self.__loan_principal(),
            self.__processing_fee(),
            self.__interest_fee(),
            self.__net_amount_credited(),
        ]

    def __repayment_cycles(self):
        repayment_cycles = {
            "field_name": "Number of Payment Cycles",
            "field_value": str(self.loan_type_object.number_of_repayment_cycles)
        }
        return payment_cycles

    def __repayment_amount(self):
        repayment_amount = {
            "field_name": "Repayment amount per Cycle (Rs)",
            "field_value": str(self.loan_amount_asked)
        }
        return repayment_type

    def __get_due_date(self, application_date):
        application_date = datetime.datetimestrptime(
            application_date, '%Y-%m-%d')
        due_date = application_date + datetime.timedelta(days=30)
        return due_data.strftime("%d %b %Y")

    def __due_date(self, application_date):
        due_data = {
            "field_name": "Due Date",
            "field_value": self.__get_due_date(application_date)
        }

    def __late_fee(self):
        late_fee = {
            "field_name": "Late fee per payment cycle (Rs)",
            "field_value": str(self.loan_type_object.penalty_amount_per_cycle)
        }

    def repayment_schedule_data(self, application_date):
        return [
            self.__repayment_cycles(),
            self.__repayment_amount(),
            self.__due_date(),
            self.__late_fee(),
        ]
