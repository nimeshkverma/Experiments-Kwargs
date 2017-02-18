from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from common.decorators import session_authorize, meta_data_response, catch_exception

from . import models, serializers

import logging
LOGGER = logging.getLogger(__name__)


class DocumentTypeList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    queryset = models.DocumentType.active_objects.all()
    serializer_class = serializers.DocumentTypeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DocumentTypeDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):
    queryset = models.DocumentType.objects.all()
    serializer_class = serializers.DocumentTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DocumentsCreate(APIView):

    parser_classes = (FormParser, MultiPartParser)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.DocumentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.check_table_conflict()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class DocumentsDetail(APIView):

    parser_classes = (FormParser, MultiPartParser)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            documents_object = get_object_or_404(models.Documents, customer_id=auth_data[
                                                 'customer_id'], document_type_id=request.query_params.get('document_type_id'))
            serializer = serializers.DocumentsSerializer(documents_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            documents_object = get_object_or_404(models.Documents, customer_id=auth_data[
                                                 'customer_id'], document_type_id=request.data.get('document_type_id'))
            serializer = serializers.DocumentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                documents_object.delete()
                serializer.check_table_conflict()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            documents_object = get_object_or_404(models.Documents, customer_id=auth_data[
                                                 'customer_id'], document_type_id=request.data.get('document_type_id'))
            documents_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class DocumentsUploadDetails(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            document_objects = models.Documents.objects.filter(
                customer_id=auth_data['customer_id'])
            response = {
                'customer_id': auth_data['customer_id'],
                'documents_uploaded': {
                    '1': False,
                    '2': False,
                    '3': False,
                    '4': False,
                    '5': False,
                }
            }
            for document_object in document_objects:
                document_type_id = document_object.document_type_id
                response['documents_uploaded'][str(document_type_id)] = True
            return Response(response, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
