from rest_framework import serializers

from . import models

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer


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


class AmountEligibleSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"}
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    class Meta:
        model = models.AmountEligible
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')
