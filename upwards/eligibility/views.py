from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers

from common.decorators import session_authorize, meta_data_response
from common.response import MetaDataResponse


class FinanceCreate(APIView):

    @meta_data_response
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.FinanceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class FinanceDetail(APIView):

    @meta_data_response
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            serializer = serializers.FinanceSerializer(finance_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @meta_data_response
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            finance_object_updated = serializers.FinanceSerializer().update(finance_object,
                                                                            request.data)
            return Response(serializers.FinanceSerializer(finance_object_updated).data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @meta_data_response
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            finance_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
