from rest_framework.views import APIView
from rest_framework import status

from . import response
from data import config_data


class Config(APIView):

    def get(self, request):
        return response.MetaDataResponse(config_data, status=status.HTTP_200_OK)
