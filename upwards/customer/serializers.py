from rest_framework import serializers

from . import models


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Customer
        exclude = ('created_at', 'updated_at', 'is_active',)
