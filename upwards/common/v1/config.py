from django.conf import settings
from common.models import OrganisationType, SalaryPaymentMode, ProfessionType
from . serializers import SalaryPaymentModeSerializer, OrganisationTypeSerializer, ProfessionTypeSerializer
from participant.models import BorrowerType
from participant.v1.serializers import BorrowerTypeSerializer
from loan.models import LoanType
from loan.v1.serializers import LoanTypeSerializer


class Config(object):
    user_state = ['unknown', 'sign_up', 'pan_submit', 'professional_submit', 'education_submit',
                  'finance_submit_email_verified', 'finance_submit_email_unverified', 'eligibility_submit',
                  'eligibility_result_approved', 'eligibility_result_rejected', 'aadhaar_submit',
                  'aadhaar_detail_submit', 'personal_contact_submit', 'document_submit_email_verified',
                  'document_submit_email_unverified', 'kyc_submit', 'kyc_result_approved',
                  'kyc_result_rejected', 'bank_detail_submit', 'loan_amount_submit',
                  'loan_application_proccessing', 'loan_application_proccessed', 'loan_application_errored']

    email_type = {
        'personal': 'customer_alternate_email',
        'professional': 'customer_profession_email'
    }

    def __init__(self):
        self.data = self.__get_data()

    def __get_base_url(self):
        return settings.BASE_URL

    def __get_versions(self):
        return settings.VERSIONS

    def __get_versioned_base_url(self):
        return settings.VERSIONED_BASE_URL

    def __get_post_otp_message(self):
        return settings.POST_OTP_MESSAGE

    def __get_profession_type(self):
        profession_type_objects = ProfessionType.objects.all()
        return ProfessionTypeSerializer(profession_type_objects, many=True).data

    def __get_borrower_type(self):
        borrower_type_objects = BorrowerType.objects.all()
        return BorrowerTypeSerializer(borrower_type_objects, many=True).data

    def __get_loan_type(self):
        loan_type_objects = LoanType.objects.all()
        return LoanTypeSerializer(loan_type_objects, many=True).data

    def __get_salary_payment_mode(self):
        salary_payment_mode_objects = SalaryPaymentMode.objects.all()
        return SalaryPaymentModeSerializer(salary_payment_mode_objects, many=True).data

    def __get_organisation_type(self):
        organisation_type_objects = OrganisationType.objects.all()
        return OrganisationTypeSerializer(organisation_type_objects, many=True).data

    def __get_customer_default_profile_pic(self):
        return settings.CUSTOMER_DEFAULT_PROFILE_PIC

    def __get_data(self):
        config_data = {
            'user_state': self.user_state,
            'base_url': self.__get_base_url(),
            'versions': self.__get_versions(),
            'versioned_base_url': self.__get_versioned_base_url(),
            'post_otp_message': self.__get_post_otp_message(),
            'email_type': self.email_type,
            'salary_payment_mode': self.__get_salary_payment_mode(),
            'organisation_type': self.__get_organisation_type(),
            'profession_type': self.__get_profession_type(),
            'borrower_type': self.__get_borrower_type(),
            'loan_type': self.__get_loan_type(),
            'customer_default_profile_pic': self.__get_customer_default_profile_pic(),
        }
        return config_data
