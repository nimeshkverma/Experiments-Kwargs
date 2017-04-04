from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response


from . import models, serializers
from common.v1.decorators import meta_data_response, catch_exception, session_authorize

import logging
LOGGER = logging.getLogger(__name__)


class LoanRequestTransactionDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.LoanRequestTransactionSerializers(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                return Response(serializer.loan_request_transactions_atomic(models.INITIATED, models.LOAN_AVAIL, models.UPWARDS), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class TransactionHistoryDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.TransactionHistorySerializers(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                return Response(serializer.transaction_history_data(), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
