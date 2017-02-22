from django.shortcuts import get_object_or_404

from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers

from common.decorators import session_authorize, meta_data_response, catch_exception
from common.response import MetaDataResponse
from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError

from activity.models import register_customer_state
from activity.model_constants import PERSONAL_CONTACT_SUBMIT_STATE

from . service.homepage_service import Homepage

import logging
LOGGER = logging.getLogger(__name__)


class CustomerList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = models.Customer.active_objects.all()
    serializer_class = serializers.CustomerSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            return self.retrieve(request, *args, **kwargs)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            response = self.update(request, *args, **kwargs)
            register_customer_state(
                PERSONAL_CONTACT_SUBMIT_STATE, auth_data['customer_id'])
            return response
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            return self.destroy(request, *args, **kwargs)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class BankDetailsCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.BankDetailsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class BankDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            bank_object = get_object_or_404(
                models.BankDetails, customer_id=auth_data['customer_id'])
            serializer = serializers.BankDetailsSerializer(bank_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            bank_object = get_object_or_404(
                models.BankDetails, customer_id=auth_data['customer_id'])
            serializers.BankDetailsSerializer().validate_foreign_keys(request.data)
            bank_object_updated = serializers.BankDetailsSerializer().update(bank_object,
                                                                             request.data)
            return Response(serializers.BankDetailsSerializer(bank_object_updated).data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            bank_object = get_object_or_404(
                models.BankDetails, customer_id=auth_data['customer_id'])
            bank_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class HomepageAPI(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            return Response(Homepage(auth_data['customer_id']).data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
