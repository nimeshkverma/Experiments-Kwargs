from social.models import Customer, Login
from social.serializers import CustomerSerializer, LoginSerializer
from rest_framework import generics


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
