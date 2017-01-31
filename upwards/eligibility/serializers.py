from rest_framework import serializers

from . import models


class FinanceSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = models.Finance
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')


class ProfessionSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    organisation_type_id = serializers.IntegerField()
    salary_payment_mode_id = serializers.IntegerField()

    class Meta:
        model = models.Profession
        exclude = ('customer', 'company', 'organisation_type',
                   'salary_payment_mode', 'created_at', 'updated_at', 'is_active', 'id')


class EducationSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    college_id = serializers.IntegerField()

    class Meta:
        model = models.Education
        exclude = ('customer', 'college', 'created_at',
                   'updated_at', 'is_active', 'id')
