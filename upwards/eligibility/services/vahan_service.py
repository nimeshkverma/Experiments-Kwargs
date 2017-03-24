import json
import requests
from django.conf import settings
from vahan_constants import VAHAN_API_MODEL_MAPPING, VAHAN_API_MODEL_RTO_MAPPING


class Vahan(object):

    def __init__(self, reg1, reg2, reg3, reg4, vertical):
        self.url = settings.VAHAN_API.format(
            reg1=reg1, reg2=reg2, reg3=reg3, reg4=reg4, vertical=vertical)
        self.vertical = vertical
        self.registration_no = (
            str(reg1) + str(reg2) + str(reg3) + str(reg4)).upper()
        self.data = {}
        self.data_fetch_success = False
        self.__get_data()

    def __get_data(self):
        response = requests.get(self.url)
        vahan_data = response.json()
        if vahan_data.get('status') in ['SUCCESS', 'success', 'Success']:
            self.data = vahan_data
            self.data_fetch_success = True

    def get_model_data(self, customer_id):
        data = {
            "customer_id": customer_id,
            "registration_no": self.registration_no,
            "vertical": self.vertical
        }
        if self.data_fetch_success:
            for api_data_key, model_key in VAHAN_API_MODEL_MAPPING.iteritems():
                if api_data_key in self.data:
                    data[model_key] = self.data[api_data_key]
            for api_data_key, model_key in VAHAN_API_MODEL_RTO_MAPPING.iteritems():
                if api_data_key in self.data.get('rto', {}):
                    data[model_key] = self.data['rto'][api_data_key]
        return data
