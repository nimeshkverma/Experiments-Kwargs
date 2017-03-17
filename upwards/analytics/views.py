from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.decorators import session_authorize, meta_data_response, catch_exception

from . import serializers

import logging
LOGGER = logging.getLogger(__name__)


class Algo360DataDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.Algo360DataSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                return Response(serializer.store_algo360_data(), status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class CreditReportDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, pk, *args, **kwargs):
        data = {'customer_id': pk}
        serializer = serializers.CreditReportSerializer(data=data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            return Response(serializer.report_data(), status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
