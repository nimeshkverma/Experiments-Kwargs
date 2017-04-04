from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views.generic import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from aadhaar import models

from common.v1.decorators import session_authorize, meta_data_response, catch_exception
from common.v1.response import MetaDataResponse
from common.v1.utils.model_utils import check_pk_existence
from common.v1.exceptions import NotAcceptableError
from customer.models import Customer

from activity.models import register_customer_state
from activity.model_constants import AADHAAR_SUBMIT_STATE, AADHAAR_DETAIL_SUBMIT_STATE
from services import loan_agreement_service

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
                response = serializer.data
                response.update(serializer.current_address_update(
                    auth_data['customer_id'], request.data))
                register_customer_state(
                    AADHAAR_SUBMIT_STATE, auth_data['customer_id'])
                return Response(response, status=status.HTTP_200_OK)
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
            response_data.update(serializer.current_address_update(
                auth_data['customer_id'], request.data))
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
            aadhaar_data_serializer = serializers.AadhaarSerializer(
                aadhaar_object_updated)
            response = aadhaar_data_serializer.data
            response.update(aadhaar_data_serializer.current_address_update(
                auth_data['customer_id'], request.data))
            return Response(response, status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            aadhaar_object = get_object_or_404(
                models.Aadhaar, customer_id=auth_data['customer_id'])
            serializer = serializers.AadhaarSerializer(aadhaar_object)
            serializer.current_address_update(
                auth_data['customer_id'], request.data, True)
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

    @catch_exception(LOGGER)
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


class AadhaarESign(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            customer_id = auth_data['customer_id']
            data = request.data
            data.update({'customer_id': customer_id})
            serializer = serializers.AadhaarESignSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.sign_data(), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class LoanAgreement(View):
    loan_agreement_template = 'aadhaar/loan_agreement.html'
    unauthorized_template = 'aadhaar/unauthorized.html'

    def get_loan_data(self, customer_id):
        return loan_agreement_service.LoanAgreement(customer_id).data

    @catch_exception(LOGGER)
    def get(self, request, pk):
        serializer = serializers.LoanAgreementSerializer(
            data={'customer_id': pk})
        if serializer.is_valid():
            if serializer.validate_foreign_keys():
                return render(request, self.loan_agreement_template, serializer.get_loan_data())
            else:
                return render(request, self.unauthorized_template)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
