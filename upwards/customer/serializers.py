from copy import deepcopy
from rest_framework import serializers

from . import models


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        exclude = ('created_at', 'updated_at', 'is_active',)


class BankDetailsSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = models.BankDetails
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')
