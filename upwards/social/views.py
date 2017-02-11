from copy import deepcopy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.decorators import session_authorize, meta_data_response

from . import serializers
from . import models


class SocialLogin(APIView):

    @meta_data_response()
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            social_login_data = serializer.save()
            return Response(social_login_data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SocialLogout(APIView):

    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            serializer = serializers.LogoutSerializer(data=auth_data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class LinkedinAuth(APIView):

    def authorize_and_parse_linkedin(self, request_data):
        processed_state = self.process_state(request_data.get('state', ''))
        request_data.update(processed_state)
        serializer = serializers.LinkedinAuthSerializer(data=request_data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_400_BAD_REQUEST)

    def process_state(self, state):
        state_raw_list = state.split(',')
        state_dict = {}
        for raw_param in state_raw_list:
            raw_param_list = raw_param.split(':')
            state_dict[raw_param_list[0]] = raw_param_list[1]
        return state_dict

    @meta_data_response()
    def get(self, request):
        request_data = deepcopy(request.GET)
        if request_data:
            return self.authorize_and_parse_linkedin(request_data)
        else:
            return Response({}, status.HTTP_200_OK)


class CustomerProfile(APIView):

    def get_linkedin_object(self,pk):
        return models.LinkedinProfile.objects.filter(customer_id=pk)

    def get_social_object(self,pk):
        return models.SocialProfile.objects.filter(customer_id=pk)

    def check_customer_exists(self,pk):
        customer = models.Login.objects.filter(pk=pk)
        if len(customer) > 0: return True
        return False

    @meta_data_response()
    def get(self, requests, pk):
        response_json = {}
        if self.check_customer_exists(pk):
            linked_profile = serializers.LinkedinAuthSerializer(data=self.get_linkedin_object(pk))
            if linked_profile.is_valid():
                response_json['linkedin'] = linked_profile.validated_data
            else:
                response_json['linkedin'] = {}

            social_profile = serializers.SocialProfileSerializer(self.get_social_object(pk),many=True)
            if social_profile:
                for social_data in social_profile.data:
                    response_json[social_data['platform']] = social_data
                if not response_json.has_key('facebook'):
                    response_json['facebook'] = {}
                if not response_json.has_key('google'):
                    response_json['google'] = {}
            else:
                response_json['facebook'] = {}
                response_json['google'] = {}

            return Response(response_json, status.HTTP_200_OK)
        else:
            return Response(response_json,status.HTTP_204_NO_CONTENT)



        
