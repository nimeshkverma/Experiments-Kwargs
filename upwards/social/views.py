from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from social.models import Customer, Login
from social.serializers import CustomerSerializer, LoginSerializer, LoginSerializerr, LogoutSerializer
from decorators import session_authorize
from social.response import MetaDataResponse


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class LoginList(generics.ListCreateAPIView):
    queryset = Login.objects.all()
    serializer_class = LoginSerializer


class LoginDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Login.objects.all()
    serializer_class = LoginSerializer


class SocialLogin(APIView):

    def post(self, request):
        serializer = LoginSerializerr(data=request.data)
        if serializer.is_valid():
            social_login_data = serializer.save()
            return MetaDataResponse(social_login_data, status=status.HTTP_200_OK)
        print serializer.errors
        return MetaDataResponse({}, status=status.HTTP_400_BAD_REQUEST)


class SocialLogout(APIView):

    @session_authorize
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            serializer = LogoutSerializer(data=auth_data)
            if serializer.is_valid():
                serializer.errors
                serializer.save()
                return MetaDataResponse({}, status.HTTP_204_NO_CONTENT)
            print serializer.errors
        return MetaDataResponse({}, status.HTTP_401_UNAUTHORIZED)
