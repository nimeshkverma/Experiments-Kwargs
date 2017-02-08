from activity.models import CustomerState
from eligibility.models import AmountEligible
from homepage_config import (ELIGIBILITY_TITLE, KYC_TITLE,
                             USER_STATES_WITH_ELIGIBILITY_AMOUNT, USER_STATE_MESSAGES)


class Homepage(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.present_state = CustomerState.get_customer_present_state(
            self.customer_id)
        self.eligibility_amount = self.__get_eligibility_amount()
        self.data = self.__get_homepage_data()

    def __get_mast_message(self):
        return "Hello User!"

    def __get_eligibility_amount(self):
        eligibility_amount = None
        if self.present_state in USER_STATES_WITH_ELIGIBILITY_AMOUNT:
            amount_eligible_objects = AmountEligible.objects.filter(
                customer_id=self.customer_id)
            if amount_eligible_objects:
                eligibility_amount = amount_eligible_objects[0].max_amount
        return eligibility_amount

    def __get_eligibility_section(self):
        message = USER_STATE_MESSAGES.get(self.present_state, {}).get(
            'eligibility', {}).get('message', '')
        if self.eligibility_amount and '{amount}' in message:
            message = message.format(amount=self.eligibility_amount)
        section = {
            'title': ELIGIBILITY_TITLE,
            'completion_percentage': USER_STATE_MESSAGES.get(self.present_state, {}).get('eligibility', {}).get('completion_percentage', 0),
            'message': message,
        }
        return section

    def __get_kyc_section(self):
        section = {
            'title': KYC_TITLE,
            'completion_percentage': USER_STATE_MESSAGES.get(self.present_state, {}).get('kyc', {}).get('completion_percentage', 0),
            'message': USER_STATE_MESSAGES.get(self.present_state, {}).get('kyc', {}).get('message', ''),
        }
        return section

    def __get_homepage_data(self):
        homepage_data = {
            'customer': {
                'id': self.customer_id,
                'state': self.present_state,
            },
            'mast_message': self.__get_mast_message(),
            'sections': {
                'eligibility': self.__get_eligibility_section(),
                'kyc': self.__get_kyc_section(),
            },
        }
        return homepage_data
