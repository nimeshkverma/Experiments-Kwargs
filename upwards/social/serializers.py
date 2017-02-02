from copy import deepcopy
from rest_framework import serializers

from . import models

from services.session_service import get_or_create_sessions


class LoginSerializer(serializers.Serializer):
    platform_token = serializers.CharField()
    source = serializers.ChoiceField(choices=models.SOURCE_CHOICES)
    platform = serializers.ChoiceField(choices=models.PLATFORM_CHOICES)

    def save(self):
        session_data = get_or_create_sessions(self.validated_data)
        return session_data


class LogoutSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    customer_id = serializers.IntegerField()

    def save(self):
        return models.Login.delete_session(self.validated_data.get(
            "session_token"), self.validated_data.get("customer_id"))


class LinkedinAuthSerializer(serializers.Serializer):
    linkedin_token = serializers.CharField()
    source = serializers.ChoiceField(choices=models.SOURCE_CHOICES)

    def save(self):
        pass
        # return create_or_update_linkedin_profile(self.validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    login_id = serializers.IntegerField()

    class Meta:
        model = models.Profile
        exclude = ('login', 'created_at', 'updated_at', 'is_active', 'id')
