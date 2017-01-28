from copy import deepcopy
from rest_framework import serializers

from . import models


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        exclude = ('created_at', 'updated_at', 'is_active',)


class BankDetailsSerializer(serializers.ModelSerializer):

    def create(self):
        validated_data = deepcopy(self.validated_data)
        validated_data["customer_id"] = models.Customer.objects.get(
            pk=validated_data["customer_id"])
        models.BankDetails.objects.create(**validated_data)
        return self.validated_data

    def update(self):
        print self.validated_data
        validated_data = deepcopy(self.validated_data)
        print validated_data
        customer_id = validated_data.pop('customer_id')
        objects_updated = models.BankDetails.objects.filter(
            pk=customer_id).update(**validated_data)
        if objects_updated:
            return self.validated_data
        return {}

    class Meta:
        model = models.BankDetails
        exclude = ('created_at', 'updated_at', 'is_active',)
