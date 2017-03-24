from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers
from common.decorators import session_authorize, meta_data_response, catch_exception

import logging
LOGGER = logging.getLogger(__name__)


class FinanceCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            finance_serializer = serializers.FinanceSerializer(
                data=request.data)
            vahan_serializer = serializers.VahanSerializer(data=request.data)
            if finance_serializer.is_valid():
                finance_serializer.validate_foreign_keys()
                finance_serializer.save()
                return Response(finance_serializer.data, status=status.HTTP_200_OK)
            return Response({'error': finance_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class FinanceDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            serializer = serializers.FinanceSerializer(finance_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            serializers.FinanceSerializer().validate_foreign_keys(request.data)
            finance_object_updated = serializers.FinanceSerializer().update(
                finance_object, request.data)
            return Response(serializers.FinanceSerializer(finance_object_updated).data, status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            finance_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class ProfessionCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.ProfessionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class ProfessionDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            profession_object = get_object_or_404(
                models.Profession, customer_id=auth_data['customer_id'])
            serializer = serializers.ProfessionSerializer(profession_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            profession_object = get_object_or_404(
                models.Profession, customer_id=auth_data['customer_id'])
            serializers.ProfessionSerializer().validate_foreign_keys(request.data)
            profession_object_updated = serializers.ProfessionSerializer().update(
                profession_object, request.data)
            return Response(serializers.ProfessionSerializer(profession_object_updated).data, status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            profession_object = get_object_or_404(
                models.Profession, customer_id=auth_data['customer_id'])
            profession_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class EducationCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.EducationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class EducationDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            education_object = get_object_or_404(
                models.Education, customer_id=auth_data['customer_id'])
            serializer = serializers.EducationSerializer(education_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            education_object = get_object_or_404(
                models.Education, customer_id=auth_data['customer_id'])
            serializers.EducationSerializer().validate_foreign_keys(request.data)
            education_object_updated = serializers.EducationSerializer().update(
                education_object, request.data)
            return Response(serializers.EducationSerializer(education_object_updated).data, status.HTTP_200_OK)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            education_object = get_object_or_404(
                models.Education, customer_id=auth_data['customer_id'])
            education_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class VahanDataDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        serializer = serializers.VahanSerializer(data=request.query_params)
        if serializer.is_valid():
            return Response(serializer.get_vahan_data(), status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VahanCreate(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.VahanSerializer(data=request.data)
            if serializer.is_valid():
                return Response(serializer.save(auth_data['customer_id']), status=status.HTTP_200_OK)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class VahanDetail(APIView):

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            vahan_object = get_object_or_404(
                models.Vahan, customer_id=auth_data['customer_id'])
            return Response(model_to_dict(vahan_object, exclude=['is_active', 'updated_at', 'created_at']), status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            serializer = serializers.VahanSerializer(data=request.data)
            if serializer.is_valid():
                updated = serializer.update(auth_data['customer_id'])
                if updated:
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    return Response({}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

    @catch_exception(LOGGER)
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            deleted = serializers.VahanSerializer().delete(
                auth_data['customer_id'])
            if deleted:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({}, status=status.HTTP_404_NOT_FOUND)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
