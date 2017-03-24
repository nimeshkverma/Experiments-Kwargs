from django.forms.models import model_to_dict
from rest_framework import serializers

from . import models

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer
from services.vahan_service import Vahan


class FinanceSerializer(serializers.ModelSerializer):
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
        model = models.Finance
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')


class ProfessionSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    organisation_type_id = serializers.IntegerField()
    salary_payment_mode_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        from common.models import Company, OrganisationType, SalaryPaymentMode
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
            {"model": Company, "pk": data.get(
                'company_id', -1), "pk_name": "company_id"},
            {"model": OrganisationType, "pk": data.get(
                'organisation_type_id', -1), "pk_name": "organisation_type_id"},
            {"model": SalaryPaymentMode, "pk": data.get(
                'salary_payment_mode_id', -1), "pk_name": "salary_payment_mode_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    class Meta:
        model = models.Profession
        exclude = ('customer', 'company', 'organisation_type',
                   'salary_payment_mode', 'created_at', 'updated_at', 'is_active', 'id')


class EducationSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    college_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        from common.models import College
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
            {"model": College, "pk": data.get(
                'college_id', -1), "pk_name": "college_id"}
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    class Meta:
        model = models.Education
        exclude = ('customer', 'college', 'created_at',
                   'updated_at', 'is_active', 'id')


class VahanSerializer(serializers.Serializer):
    reg1 = serializers.CharField()
    reg2 = serializers.CharField()
    reg3 = serializers.CharField()
    reg4 = serializers.CharField()
    vertical = serializers.CharField()

    def get_vahan_data(self):
        vahan = Vahan(**self.validated_data)
        data = {
            'valid_registration_id': False,
            'vahan_data': {}
        }
        if vahan.data_fetch_success:
            data['vahan_data'] = vahan.data
            data['valid_registration_id'] = vahan.data_fetch_success
        return data

    def get_customer_vahan_data(self, customer_id):
        vahan_object = models.Vahan.objects.get(customer_id=customer_id)
        return model_to_dict(vahan_object, exclude=['is_active', 'updated_at', 'created_at'])

    def save(self, customer_id):
        vahan = Vahan(**self.validated_data)
        model_data = vahan.get_model_data(customer_id)
        models.Vahan.objects.create(**model_data)
        return model_data

    def update(self, customer_id):
        updated = True
        vahan = Vahan(**self.validated_data)
        model_data = vahan.get_model_data(customer_id)
        model_data.pop('customer_id')
        updated_objects = models.Vahan.objects.filter(
            customer_id=customer_id).update(**model_data)
        if not updated_objects:
            updated = False
        return updated

    def delete(self, customer_id):
        deleted = True
        deleted_objects = models.Vahan.objects.filter(
            customer_id=customer_id).delete()
        if not deleted_objects:
            deleted = False
        return deleted
