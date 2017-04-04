from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from . import models, serializers
from common.v1.decorators import meta_data_response, catch_exception, thirdparty_authorize

import logging
LOGGER = logging.getLogger(__name__)


class ThirdPartyLeadList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = models.ThirdPartyLead.active_objects.all()
    serializer_class = serializers.ThirdPartyLeadSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def get(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            return self.list(request, *args, **kwargs)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def post(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            return self.create(request, *args, **kwargs)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)


class ThirdPartyLeadDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = models.ThirdPartyLead.objects.all()
    serializer_class = serializers.ThirdPartyLeadSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def get(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def put(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            return self.update(request, *args, **kwargs)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def delete(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)


class ThirdPartyLeadDocumentsCreate(APIView):

    parser_classes = (FormParser, MultiPartParser)

    @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def post(self, request, third_party_auth, *args, **kwargs):
        if third_party_auth:
            serializer = serializers.ThirdPartyLeadDocumentsSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.check_table_conflict()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)


class ThirdPartyLeadDocumentsDetail(APIView):

    parser_classes = (FormParser, MultiPartParser)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def get(self, request, third_party_auth, pk, *args, **kwargs):
        if third_party_auth:
            documents_object = get_object_or_404(
                models.Documents, customer_id=pk, document_type=request.query_params.get('document_type'))
            serializer = serializers.ThirdPartyLeadDocumentsSerializer(
                documents_object)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def put(self, request, third_party_auth, pk, *args, **kwargs):
        if third_party_auth:
            documents_object = get_object_or_404(
                models.Documents, customer_id=pk, document_type=request.data.get('document_type'))
            serializer = serializers.ThirdPartyLeadDocumentsSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                documents_object.delete()
                serializer.check_table_conflict()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)

    # @catch_exception(LOGGER)
    @meta_data_response()
    @thirdparty_authorize()
    def delete(self, request, third_party_auth, pk, *args, **kwargs):
        if third_party_auth:
            documents_object = get_object_or_404(
                models.Documents, customer_id=pk, document_type=request.data.get('document_type'))
            documents_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({}, status.HTTP_401_UNAUTHORIZED)
