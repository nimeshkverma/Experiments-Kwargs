from analytics.models import Algo360
from eligibility.models import Profession
from analytics_service_constants import CREDIT_LIMIT_VARIABLES, CREDIT_REPORT_MAPPING


class CustomerCreditLimit(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __get_minimum_average_balance(self, algo360_object):
        minimum_average_balance_list = []
        for minimum_average_balance_key in CREDIT_LIMIT_VARIABLES:
            minimum_average_balance_list.append(
                algo360_object.__dict__.get(minimum_average_balance_key, 0))
        return min(minimum_average_balance_list) if minimum_average_balance_list else 0

    def get_limit(self):
        minimum_average_balance = None
        salary = None
        algo360_objects = Algo360.objects.filter(customer_id=self.customer_id)
        if algo360_objects:
            minimum_average_balance = self.__get_minimum_average_balance(algo360_objects[
                                                                         0])
        profession_objects = Profession.objects.filter(
            customer_id=self.customer_id)
        if profession_objects:
            salary = profession_objects[0].salary
        if minimum_average_balance == None and salary == None:
            return 0
        elif minimum_average_balance == None:
            return salary / 3
        elif salary == None:
            return minimum_average_balance / 3
        else:
            return min(salary, minimum_average_balance) / 3


class CreditReport(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.customer_credit_limit = CustomerCreditLimit(
            self.customer_id).get_limit()
        self.data = self.__get_report_data()

    def __get_algo360_data(self):
        data = {key: None for key in CREDIT_REPORT_MAPPING['Algo360'].values()}
        data['credit_limit'] = self.customer_credit_limit
        algo360_objects = Algo360.objects.filter(customer_id=self.customer_id)
        if algo360_objects:
            for data_key, data_value in algo360_objects[0].__dict__.iteritems():
                if data_key in CREDIT_REPORT_MAPPING['Algo360'].keys():
                    data[CREDIT_REPORT_MAPPING['Algo360'][data_key]] = data_value
        return data

    def __get_professional_data(self):
        data = {key: None for key in CREDIT_REPORT_MAPPING[
            'Profession'].values()}
        profession_objects = Profession.objects.filter(
            customer_id=self.customer_id)
        if profession_objects:
            for data_key, data_value in profession_objects[0].__dict__.iteritems():
                if data_key in CREDIT_REPORT_MAPPING['Profession'].keys():
                    data[CREDIT_REPORT_MAPPING['Profession']
                         [data_key]] = data_value
        return data

    def __get_derived_data(self, report_data):
        derived_data = {}
        credit_card_last_payment_due = report_data.get(
            'credit_card_last_payment_due', 1) if report_data.get('credit_card_last_payment_due', 1) else 1
        derived_data['leverage'] = round(report_data.get(
            'monthly_average_balance_lifetime', 0) * 1.0 / credit_card_last_payment_due, 3)
        return derived_data

    def __get_report_data(self):
        report_data = self.__get_algo360_data()
        report_data.update(self.__get_professional_data())
        report_data.update(self.__get_derived_data(report_data))
        return report_data
