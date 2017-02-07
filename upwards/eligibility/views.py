from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models, serializers
from common.decorators import session_authorize, meta_data_response, catch_exception


class FinanceCreate(APIView):

    @catch_exception
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.FinanceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class FinanceDetail(APIView):

    @catch_exception
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            finance_object = get_object_or_404(
                models.Finance, customer_id=auth_data['customer_id'])
            serializer = serializers.FinanceSerializer(finance_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception
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

    @catch_exception
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

    @catch_exception
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.ProfessionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print serializer.errors
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class ProfessionDetail(APIView):

    @catch_exception
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            profession_object = get_object_or_404(
                models.Profession, customer_id=auth_data['customer_id'])
            serializer = serializers.ProfessionSerializer(profession_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception
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

    @catch_exception
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

    @catch_exception
    @meta_data_response()
    @session_authorize('customer_id')
    def post(self, request, auth_data):
        if auth_data.get('authorized'):
            serializer = serializers.EducationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validate_foreign_keys()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class EducationDetail(APIView):

    @catch_exception
    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            education_object = get_object_or_404(
                models.Education, customer_id=auth_data['customer_id'])
            serializer = serializers.EducationSerializer(education_object)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @catch_exception
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

    @catch_exception
    @meta_data_response()
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get('authorized'):
            education_object = get_object_or_404(
                models.Education, customer_id=auth_data['customer_id'])
            education_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class AmountEligibleCreate(APIView):

    @catch_exception
    @meta_data_response()
    def post(self, request):
        serializer = serializers.AmountEligibleSerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AmountEligibleDetail(APIView):

    @catch_exception
    @meta_data_response()
    def get(self, request, pk):
        amount_eligible_object = get_object_or_404(
            models.AmountEligible, customer_id=pk)
        serializer = serializers.AmountEligibleSerializer(
            amount_eligible_object)
        return Response(serializer.data, status.HTTP_200_OK)

    @catch_exception
    @meta_data_response()
    def put(self, request, pk):
        amount_eligible_object = get_object_or_404(
            models.AmountEligible, customer_id=pk)
        serializers.AmountEligibleSerializer().validate_foreign_keys(request.data)
        amount_eligible_object_updated = serializers.AmountEligibleSerializer().update(
            amount_eligible_object, request.data)
        return Response(serializers.AmountEligibleSerializer(amount_eligible_object_updated).data, status.HTTP_200_OK)

    @catch_exception
    @meta_data_response()
    def delete(self, request, pk):
        amount_eligible_object = get_object_or_404(
            models.AmountEligible, customer_id=pk)
        amount_eligible_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
