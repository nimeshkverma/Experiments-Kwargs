from analytics.models import Algo360
from eligibility.models import Profession
from algo360_constants import ALGO360_UPWARDS_MAPPING


class CustomerCreditLimit(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __get_minimum_average_balance(self, algo360_object):
        minimum_average_balance_list = []
        for minimum_average_balance_key in ALGO360_UPWARDS_MAPPING.values():
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
