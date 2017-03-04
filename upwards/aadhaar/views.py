from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers

from common.decorators import session_authorize, meta_data_response, catch_exception
from common.response import MetaDataResponse
from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer

from activity.models import register_customer_state
from activity.model_constants import AADHAAR_SUBMIT_STATE, AADHAAR_DETAIL_SUBMIT_STATE

import logging
LOGGER = logging.getLogger(__name__)


class AadhaarCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.AadhaarSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                register_customer_state(
                    AADHAAR_SUBMIT_STATE, auth_data['customer_id'])
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class AadhaarDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            aadhaar_object = get_object_or_404(
                models.Aadhaar, customer_id=auth_data['customer_id'])
            serializer = serializers.AadhaarSerializer(aadhaar_object)
            response_data = serializer.data
            response_data.update({
                'editable_fields': ['mother_first_name', 'mother_last_name', 'mobile_no']
            })
            return Response(response_data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            aadhaar_object = get_object_or_404(
                models.Aadhaar, customer_id=auth_data['customer_id'])
            serializers.AadhaarSerializer().validate_foreign_keys(request.data)
            aadhaar_object_updated = serializers.AadhaarSerializer().update(
                aadhaar_object, request.data)
            register_customer_state(
                AADHAAR_DETAIL_SUBMIT_STATE, aadhaar_object_updated.customer_id)
            return Response(serializers.AadhaarSerializer(aadhaar_object_updated).data, status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            aadhaar_object = get_object_or_404(
                models.Aadhaar, customer_id=auth_data['customer_id'])
            aadhaar_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class AadhaarOTP(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            serializer = serializers.AadhaarOTPSerializer(
                data=request.query_params)
            if serializer.is_valid():
                return Response(serializer.otp_data(), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class AadhaarEKYC(APIView):

    # @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            customer_id = auth_data['customer_id']
            data = request.data
            data.update({'customer_id': customer_id})
            serializer = serializers.AadhaarEKYCSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.kyc_data(), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
