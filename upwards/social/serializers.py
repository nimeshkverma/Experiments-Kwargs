from rest_framework import serializers

from . import models

from services.session_service import get_or_create_sessions


class LoginSerializer(serializers.Serializer):
    platform_token = serializers.CharField()
    source = serializers.ChoiceField(choices=models.SOURCE_CHOICES)
    platform = serializers.ChoiceField(choices=models.PLATFORM_CHOICES)

    def save(self):
        return get_or_create_sessions(self.validated_data)


class LogoutSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    customer_id = serializers.IntegerField()

    def save(self):
        return models.Login.delete_session(self.validated_data.get(
            "session_token"), self.validated_data.get("customer_id"))
