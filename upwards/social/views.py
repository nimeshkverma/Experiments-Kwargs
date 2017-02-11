from copy import deepcopy
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.decorators import session_authorize, meta_data_response

from . import serializers


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
