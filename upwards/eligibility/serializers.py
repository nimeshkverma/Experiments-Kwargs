from copy import deepcopy
from rest_framework import serializers

from . import models
from customer.models import Customer


class FinanceSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = models.Finance
        exclude = ('customer', 'created_at', 'updated_at', 'is_active', 'id')
