from rest_framework import mixins, generics, status
from rest_framework.response import Response

from . import models, serializers

from common.decorators import session_authorize, meta_data_response
from common.response import MetaDataResponse


class CustomerList(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = models.Customer.active_objects.all()
    serializer_class = serializers.CustomerSerializer

    @meta_data_response
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @meta_data_response
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomerDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    @meta_data_response
    @session_authorize()
    def get(self, request, auth_data, *args, **kwargs):
        if auth_data.get("authorized"):
            return self.retrieve(request, *args, **kwargs)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @meta_data_response
    @session_authorize()
    def put(self, request, auth_data, *args, **kwargs):
        if auth_data.get("authorized"):
            return self.update(request, *args, **kwargs)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @meta_data_response
    @session_authorize()
    def delete(self, request, auth_data, *args, **kwargs):
        if auth_data.get("authorized"):
            return self.destroy(request, *args, **kwargs)
        return Response({}, status.HTTP_401_UNAUTHORIZED)
