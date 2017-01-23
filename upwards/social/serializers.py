from rest_framework import serializers
from social.models import Customer, Login


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = '__all__'
#     def create(self, validated_data):
#         return Login.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

# 'customer','email_id','platform','source','social_data','platform_token'
