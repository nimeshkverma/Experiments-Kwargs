import json

from rest_framework import serializers

from models import Customer, Login, PLATFORM_CHOICES, SOURCE_CHOICES
from services.social_service import SocialProfile
from services.session_service import get_or_create_sessionss


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


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = '__all__'


class LoginSerializerr(serializers.Serializer):
    platform_token = serializers.CharField()
    source = serializers.ChoiceField(choices=SOURCE_CHOICES)
    platform = serializers.ChoiceField(choices=PLATFORM_CHOICES)

    def save(self):
        return get_or_create_sessionss(self.validated_data)

    # def saved(self):
    #     social_profile = SocialProfile(self.validated_data.get(
    #         "platform"), self.validated_data.get("platform_token"))
    #     email_related_sessions = Login.email_related_logins(
    #         social_profile.email_id)
    #     if email_related_sessions:
    #         platform_dict = {
    #             "facebook": None,
    #             "google": None
    #         }
    #         for customer in email_related_sessions:
    #             print customer
    #             platform_dict[customer.platform] = customer

    #         if platform_dict.get(self.validated_data.get("platform_token")):
    #             return {"session_token": platform_dict[self.validated_data["platform"]].session_token, "customer_id": platform_dict[self.validated_data["platform"]].customer_id}
    #         else:
    #             print platform_dict
    #             new_customer = email_related_sessions[0]
    #             new_customer.id = None
    #             new_customer.platform = self.validated_data.get("platform")
    #             new_customer.platform_token = self.validated_data.get(
    #                 "platform_token")
    #             new_customer.save()
    #         return {"session_token": new_customer.session_token, "customer_id": new_customer.customer_id}
    #     else:
    #         new_customer = Customer.objects.create()
    #         login_object_dict = {
    #             "platform_token": self.validated_data['platform_token'],
    #             "source": self.validated_data['source'],
    #             "platform": self.validated_data['platform'],
    #             "customer": new_customer,
    #             "social_data": json.dumps(social_profile.data),
    #             "email_id": social_profile.email_id,
    #             "session_token": "upwards_" + str(new_customer.customer_id) + "_" + get_random_string(length=32)
    #         }
    #         new_customer = Login.objects.create(**login_object_dict)
    # return {"session_token": new_customer.session_token, "customer_id":
    # new_customer.customer_id}


class LogoutSerializer(serializers.Serializer):
    session_token = serializers.CharField(max_length=64)
    customer_id = serializers.IntegerField()

    def save(self):
        return Login.delete_session(self.validated_data.get(
            "session_token"), self.validated_data.get("customer_id"))
