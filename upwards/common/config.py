from django.conf import settings
from . models import OrganisationType, SalaryPaymentMode
from . serializers import SalaryPaymentModeSerializer, OrganisationTypeSerializer


class Config(object):
    USER_STATE = {
        "KYC": {
            "personal": 75,
            "not_started": 0,
            "AADHAR": 25,
            "AADHAR_details": 50,
            "uploads": 100
        },
        "eligiblity": {
            "professional": 50,
            "not_started": 0,
            "education": 75,
            "miscellaneous": 100,
            "PAN": 25
        }
    }

    EMAIL_TYPE = {
        "personal": "customer_altername_email",
        "professional": "customer_profession_email"
    }

    def __init__(self):
        self.data = self.__get_data()

    def __get_base_url(self):
        return settings.BASE_URL

    def __get_post_otp_message(self):
        return settings.POST_OTP_MESSAGE

    def __get_salary_payment_mode(self):
        salary_payment_mode_objects = SalaryPaymentMode.objects.all()
        return SalaryPaymentModeSerializer(salary_payment_mode_objects, many=True).data

    def __get_organisation_type(self):
        organisation_type_objects = OrganisationType.objects.all()
        return OrganisationTypeSerializer(organisation_type_objects, many=True).data

    def __get_data(self):
        config_data = {
            "USER_STATE": self.USER_STATE,
            "BASE_URL": self.__get_base_url(),
            "POST_OTP_MESSAGE": self.__get_post_otp_message(),
            "EMAIL_TYPE": self.EMAIL_TYPE,
            "SALARY_PAYMENT_MODE": self.__get_salary_payment_mode(),
            "ORGANISATION_TYPE": self.__get_organisation_type()
        }
        return config_data
