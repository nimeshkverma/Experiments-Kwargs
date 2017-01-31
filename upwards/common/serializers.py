from rest_framework import serializers

from social.models import Login
from . import models


class AuthenticationSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    customer_id = serializers.IntegerField()

    def verify_and_update_session(self):
        login_object = Login.customer_and_session_login(self.validated_data.get(
            "session_token"), self.validated_data.get("customer_id"))
        if not login_object:
            return False
        else:
            login_object.save()
            return True


class CollegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.College
        fields = ('id', 'name', 'is_active')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        fields = ('id', 'name', 'is_active')


class SalaryPaymentModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SalaryPaymentMode
        fields = ('id', 'name', 'is_active')


class OrganisationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrganisationType
        fields = ('id', 'name', 'is_active')
