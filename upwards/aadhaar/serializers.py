from rest_framework import serializers

from . import models

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer
from services.ekyc_service import EKYC


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
        return otp_generation_data
