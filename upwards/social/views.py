from rest_framework.views import APIView
from rest_framework import status

from . import serializers

from common.decorators import session_authorize
from common.response import MetaDataResponse


class SocialLogin(APIView):

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            social_login_data = serializer.save()
            return MetaDataResponse(social_login_data, status=status.HTTP_200_OK)
        return MetaDataResponse({}, status=status.HTTP_400_BAD_REQUEST)


class SocialLogout(APIView):

    @session_authorize
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            serializer = serializers.LogoutSerializer(data=auth_data)
            if serializer.is_valid():
                serializer.errors
                serializer.save()
                return MetaDataResponse({}, status.HTTP_204_NO_CONTENT)
        return MetaDataResponse({}, status.HTTP_401_UNAUTHORIZED)
