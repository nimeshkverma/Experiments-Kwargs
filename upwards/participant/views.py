from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers
from common.decorators import session_authorize, meta_data_response, catch_exception

import logging
LOGGER = logging.getLogger(__name__)


class BorrowerCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request):
        serializer = serializers.BorrowerSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print serializer.errors
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class BorrowerDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, pk):
        borrower_object = get_object_or_404(
            models.Borrower, customer_id=pk)
        serializer = serializers.BorrowerSerializer(
            borrower_object)
        return Response(serializer.data, status.HTTP_200_OK)

    @catch_exception(LOGGER)
    @meta_data_response()
    def put(self, request, pk):
        borrower_object = get_object_or_404(
            models.Borrower, customer_id=pk)
        serializers.BorrowerSerializer().validate_foreign_keys(request.data)
        borrower_object_updated = serializers.BorrowerSerializer().update(
            borrower_object, request.data)
        return Response(serializers.BorrowerSerializer(borrower_object_updated).data, status.HTTP_200_OK)

    @catch_exception(LOGGER)
    @meta_data_response()
    def delete(self, request, pk):
        borrower_object = get_object_or_404(
            models.Borrower, customer_id=pk)
        borrower_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
