from rest_framework import serializers

from . import models


class LoanTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LoanType
        exclude = ('created_at', 'updated_at')
