from django.conf import settings
from . models import OrganisationType, SalaryPaymentMode
from . serializers import SalaryPaymentModeSerializer, OrganisationTypeSerializer


class Config(object):
    user_state = ['unknown', 'sign_up', 'pan_submit', 'professional_submit', 'education_submit',
                  'finance_submit_email_verified', 'finance_submit_email_unverified', 'eligibility_submit',
                  'eligibility_result_approved', 'eligibility_result_rejected', 'aadhaar_submit',
                  'aadhaar_detail_submit', 'personal_contact_submit', 'document_submit_email_verified',
                  'document_submit_email_unverified', 'kyc_submit', 'kyc_result_approved',
                  'kyc_result_rejected', 'bank_detail_submit', 'loan_amount_submit',
                  'loan_application_proccessing', 'loan_application_proccessed', 'loan_application_errored']

    email_type = {
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
            "user_state": self.user_state,
            "base_url": self.__get_base_url(),
            "post_otp_message": self.__get_post_otp_message(),
            "email_type": self.email_type,
            "salary_payment_mode": self.__get_salary_payment_mode(),
            "organisation_type": self.__get_organisation_type()
        }
        return config_data
