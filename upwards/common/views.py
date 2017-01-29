from rest_framework.views import APIView
from rest_framework import status, mixins, generics

from . import response, models, serializers
from decorators import meta_data_response
from data import config_data


class Config(APIView):

    def get(self, request):
        return response.MetaDataResponse(config_data, status=status.HTTP_200_OK)


class CollegeList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = models.College.active_objects.all()
    serializer_class = serializers.CollegeSerializer

    @meta_data_response
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @meta_data_response
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

    @meta_data_response
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @meta_data_response
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
