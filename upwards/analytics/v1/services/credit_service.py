from analytics.models import Algo360
from eligibility.models import Profession
from analytics_service_constants import MAB_VARIABLES, SALARY_VARIABLE, CREDIT_REPORT_MAPPING
from django.conf import settings


class CustomerCreditLimit(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.limit = self.__get_limit()
        self.is_eligible = self.__is_eligible()

    def __get_minimum_average_balance(self, algo360_object):
        minimum_average_balance_list = []
        for minimum_average_balance_key in MAB_VARIABLES:
            if algo360_object.__dict__.get(minimum_average_balance_key, 0) != 'N.A':
                minimum_average_balance_list.append(
                    int(float(algo360_object.__dict__.get(minimum_average_balance_key, 0))))
        return min(minimum_average_balance_list) if minimum_average_balance_list else None

    def __get_algo360_salary(self, algo360_object):
        return algo360_object.__dict__.get(SALARY_VARIABLE) if algo360_object.__dict__.get(SALARY_VARIABLE) != 'N.A' else None

    def __get_limit_from_variables(self, salary, algo360_salary, minimum_average_balance):
        limit = 0
        if algo360_salary == None and minimum_average_balance == None:
            limit = salary / settings.CREDIT_ELIGIBILITY_FACTOR if salary else 0
        elif algo360_salary == None:
            if minimum_average_balance:
                limit = min(salary, minimum_average_balance) / \
                    settings.CREDIT_ELIGIBILITY_FACTOR if salary else minimum_average_balance / \
                    settings.CREDIT_ELIGIBILITY_FACTOR
            else:
                limit = salary / settings.CREDIT_ELIGIBILITY_FACTOR if salary else 0
        elif minimum_average_balance == None:
            if algo360_salary:
                limit = min(algo360_salary, salary) / \
                    settings.CREDIT_ELIGIBILITY_FACTOR if salary else algo360_salary / \
                    settings.CREDIT_ELIGIBILITY_FACTOR
            else:
                limit = salary / settings.CREDIT_ELIGIBILITY_FACTOR if salary else 0
        else:
            limit = min(min(algo360_salary, minimum_average_balance), salary) / \
                settings.CREDIT_ELIGIBILITY_FACTOR if salary else min(
                algo360_salary, minimum_average_balance) / settings.CREDIT_ELIGIBILITY_FACTOR
        return int(limit)

    def __get_limit(self):
        minimum_average_balance = None
        algo360_salary = None
        salary = None
        algo360_objects = Algo360.objects.filter(customer_id=self.customer_id)
        if algo360_objects:
            minimum_average_balance = self.__get_minimum_average_balance(algo360_objects[
                                                                         0])
            algo360_salary = self.__get_algo360_salary(algo360_objects[0])
        profession_objects = Profession.objects.filter(
            customer_id=self.customer_id)

        if profession_objects:
            salary = profession_objects[0].salary
        return self.__get_limit_from_variables(salary, algo360_salary, minimum_average_balance)

    def __is_eligible(self):
        is_eligible = False
        if self.limit >= settings.ELIGIBILITY_LIMIT['lower']:
            is_eligible = True
        return is_eligible


class CreditReport(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.customer_credit_limit = CustomerCreditLimit(
            self.customer_id).limit
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
            'credit_card_last_payment_due', 'N.A') if report_data.get('credit_card_last_payment_due') else 'N.A'
        if credit_card_last_payment_due == 'N.A' or report_data.get('monthly_average_balance_lifetime') == 'N.A':
            derived_data['leverage'] = 'N.A'
        else:
            derived_data['leverage'] = round(float(report_data.get(
                'monthly_average_balance_lifetime', 0)) * 1.0 / credit_card_last_payment_due, 3)
        return derived_data

    def __get_report_data(self):
        report_data = self.__get_algo360_data()
        report_data.update(self.__get_professional_data())
        report_data.update(self.__get_derived_data(report_data))
        return report_data
