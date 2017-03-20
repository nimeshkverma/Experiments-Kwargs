from rest_framework import serializers

from . import models

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer
from social.models import Login
from services import algo360_service, credit_service


class Algo360DataSerializer(serializers.ModelSerializer):
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

    def store_algo360_data(self):
        algo360_data = {}
        login_objects = Login.objects.filter(
            customer_id=self.validated_data.get('customer_id', -1))
        if login_objects:
            imei = login_objects[0].imei
            customer_data = {
                'imei': imei,
                'customer_id': self.validated_data.get('customer_id')
            }
            algo360 = algo360_service.Algo360(
                self.validated_data.get('customer_id'))
            algo360_data.update(algo360.get_model_data())
            algo360_objects = models.Algo360.objects.filter(
                customer_id=self.validated_data.get('customer_id', -1))
            if algo360_objects:
                models.Algo360.objects.filter(
                    customer_id=self.validated_data.get('customer_id')).update(**algo360_data)
                algo360_data.update(customer_data)
            else:
                algo360_data.update(customer_data)
                models.Algo360.objects.create(**algo360_data)
        if algo360_data:
            algo360_data.update({'data_saved': True})
        else:
            algo360_data.update({'data_saved': False})
        return algo360_data

    class Meta:
        model = models.Algo360
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')


class CreditReportSerializer(serializers.Serializer):
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

    def report_data(self):
        return credit_service.CreditReport(self.validated_data.get('customer_id')).data
