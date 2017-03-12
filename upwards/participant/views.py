from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers
from common.decorators import session_authorize, meta_data_response, catch_exception
from analytics.services.credit_limit_service import CustomerCreditLimit

import logging
LOGGER = logging.getLogger(__name__)


class BorrowerCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            data = {'credit_limit': CustomerCreditLimit(
                auth_data['customer_id']).get_limit()}
            data.update(request.data)
            print data
            serializer = serializers.BorrowerSerializer(
                data=data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


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


class BorrowerTypeList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = models.BorrowerType.active_objects.all()
    serializer_class = serializers.BorrowerTypeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BorrowerTypeDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = models.BorrowerType.objects.all()
    serializer_class = serializers.BorrowerTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class LenderList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = models.Lender.active_objects.all()
    serializer_class = serializers.LenderSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class LenderDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = models.Lender.objects.all()
    serializer_class = serializers.LenderSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
