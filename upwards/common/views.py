from rest_framework.views import APIView
from rest_framework import status, mixins, generics

from . import response, models, serializers
from decorators import meta_data_response, catch_exception
import config

import logging
LOGGER = logging.getLogger(__name__)


class Config(APIView):

    def get(self, request):
        return response.MetaDataResponse(config.Config().data, status=status.HTTP_200_OK)


class CollegeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = models.College.active_objects.all()
    serializer_class = serializers.CollegeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CollegeDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = models.College.objects.all()
    serializer_class = serializers.CollegeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CompanyList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = models.Company.active_objects.all()
    serializer_class = serializers.CompanySerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CompanyDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SalaryPaymentModeList(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = models.SalaryPaymentMode.active_objects.all()
    serializer_class = serializers.SalaryPaymentModeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SalaryPaymentModeDetail(mixins.RetrieveModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin,
                              generics.GenericAPIView):
    queryset = models.SalaryPaymentMode.objects.all()
    serializer_class = serializers.SalaryPaymentModeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class OrganisationTypeList(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           generics.GenericAPIView):
    queryset = models.OrganisationType.active_objects.all()
    serializer_class = serializers.OrganisationTypeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrganisationTypeDetail(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             generics.GenericAPIView):
    queryset = models.OrganisationType.objects.all()
    serializer_class = serializers.OrganisationTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProfessionTypeList(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         generics.GenericAPIView):
    queryset = models.ProfessionType.active_objects.all()
    serializer_class = serializers.ProfessionTypeSerializer

    @catch_exception(LOGGER)
    @meta_data_response()
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @catch_exception(LOGGER)
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        print request.data
        return self.create(request, *args, **kwargs)


class ProfessionTypeDetail(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = models.ProfessionType.objects.all()
    serializer_class = serializers.ProfessionTypeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
