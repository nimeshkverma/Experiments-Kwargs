from rest_framework import serializers

from . import models


class AadhaarSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()

    class Meta:
        model = models.Aadhaar
        exclude = ('customer', 'created_at',
                   'updated_at', 'is_active', 'id')
