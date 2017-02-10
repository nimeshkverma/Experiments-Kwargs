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
        # serializer = serializer.LinkedinAuthSerializer(request_data)
        # if serializer.is_valid():
        #     serializer.authorize()
        return Response(request_data, status.HTTP_200_OK)
        # return Response({}, status.HTTP_400_BAD_REQUEST)

    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            return self.authorize_and_parse_linkedin(request.data)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data):
        if auth_data.get("authorized"):
            return self.authorize_and_parse_linkedin(request.GET)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
