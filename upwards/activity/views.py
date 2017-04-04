from copy import deepcopy
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers

from common.v1.decorators import session_authorize, meta_data_response, catch_exception
from common.v1.exceptions import NotAcceptableError


from activity.models import register_customer_state
from activity.model_constants import (ELIGIBILITY_SUBMIT_STATE,
                                      ELIGIBILITY_RESULT_REJECTED_STATE,
                                      DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE,
                                      KYC_SUBMIT_STATE,
                                      DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE,
                                      KYC_RESULT_REJECTED_STATE,
                                      KYC_RESULT_APPROVED_STATE,)

import logging
LOGGER = logging.getLogger(__name__)


class CustomerStateChange(APIView):

    allowed_states = [ELIGIBILITY_SUBMIT_STATE, ELIGIBILITY_RESULT_REJECTED_STATE, KYC_RESULT_APPROVED_STATE,
                      DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE, KYC_SUBMIT_STATE, KYC_RESULT_REJECTED_STATE]

    def is_personal_email_verified(self, customer_id):
        from customer.models import Customer
        from messenger.models import EmailVerification, PERSONAL

        customer_object = Customer.objects.get(customer_id=customer_id)
        if customer_object.is_alternate_email_id_verified:
            return True
        email_objects = EmailVerification.objects.filter(
            customer_id=customer_id, email_id=customer_object.alternate_email_id, email_type=PERSONAL)
        if email_objects and email_objects[0].is_verified:
            return True
        return False

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            customer_id = auth_data['customer_id']
            data = request.data
            data.update({'customer_id': customer_id})
            serializer = serializers.CustomerStateSerializer(
                data=data)
            if serializer.is_valid():
                present_state = serializer.data.get('present_state')
                if (present_state in self.allowed_states):
                    serializer.validate_foreign_keys()
                    if present_state == DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE:
                        if not self.is_personal_email_verified(customer_id):
                            present_state = DOCUMENT_SUBMIT_EMAIL_UNVERIFIED_STATE
                    register_customer_state(present_state, customer_id)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            customer_state_object = get_object_or_404(
                models.CustomerState, customer_id=auth_data['customer_id'])
            serializer = serializers.CustomerStateSerializer(
                customer_state_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
