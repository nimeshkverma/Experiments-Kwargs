from rest_framework import serializers

from . import models

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer
from services.ekyc_service import EKYC
from services.esign_service import ESign
from services.loan_agreement_service import LoanAgreement


CURRENT_ADDRESS_DICT = {
    'current_address_line1': None,
    'current_address_line2': None,
    'current_city': None,
    'current_state': None,
    'current_pincode': None,
}


class AadhaarSerializer(serializers.ModelSerializer):

    customer_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def current_address_update(self, customer_id, data, delete=False):
        updation_dict = {current_address_key: data.get(
            current_address_key) for current_address_key in CURRENT_ADDRESS_DICT} if not delete else CURRENT_ADDRESS_DICT
        Customer.objects.filter(
            customer_id=customer_id).update(**updation_dict)
        customer_dict = Customer.objects.get(customer_id=customer_id).__dict__
        return {current_address_key: customer_dict.get(current_address_key) for current_address_key in CURRENT_ADDRESS_DICT}

    class Meta:
        model = models.Aadhaar
        exclude = ('customer', 'created_at',
                   'updated_at', 'is_active', 'id')


class AadhaarOTPSerializer(serializers.Serializer):
    aadhaar = serializers.CharField(
        max_length=12, min_length=12, allow_blank=False)
    service_type = serializers.CharField(
        max_length=16, min_length=1, allow_blank=False)

    def otp_data(self):
        otp_generation_data = {
            'otp_generation_successful': False
        }
        if self.validated_data.get('service_type') in ['ekyc', 'Ekyc', 'EKYC']:
            ekyc = EKYC(self.validated_data.get('aadhaar'))
            otp_generation_data[
                'otp_generation_successful'] = ekyc.generate_otp()
        elif self.validated_data.get('service_type') in ['esign', 'Esign', 'ESIGN']:
            esign = ESign(self.validated_data.get('aadhaar'))
            otp_generation_data[
                'otp_generation_successful'] = esign.generate_otp()
        return otp_generation_data


class AadhaarEKYCSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    aadhaar = serializers.CharField(
        max_length=12, min_length=12, allow_blank=False)
    otp = serializers.CharField(
        max_length=6, min_length=6, allow_blank=False)

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def kyc_data(self):
        data = {}
        ekyc = EKYC(self.validated_data.get('aadhaar'))
        ekyc.get_kyc_data(self.validated_data.get('otp'))
        ekyc.update_aadhaar_table(self.validated_data.get('customer_id'))
        ekyc.upload_document(self.validated_data.get('customer_id'))
        return data


class AadhaarESignSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    aadhaar = serializers.CharField(
        max_length=12, min_length=12, allow_blank=False)
    otp = serializers.CharField(
        max_length=6, min_length=6, allow_blank=False)

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def sign_data(self):
        esign = ESign(self.validated_data.get('aadhaar'))
        data = esign.generate_and_sign_aggrement(self.validated_data.get(
            'otp'), self.validated_data.get('customer_id'))
        return data


class LoanAgreementSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        valid_data = False
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if check_pk_existence(model_pk['model'], model_pk['pk']):
                    valid_data = True
        return valid_data

    def get_loan_data(self):
        return LoanAgreement(self.validated_data.get('customer_id')).data
