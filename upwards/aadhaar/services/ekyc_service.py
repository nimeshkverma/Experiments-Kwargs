try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import datetime
import requests
from django.conf import settings


class EKYC(object):

    def __init__(self, aadhaar):
        self.__aadhaar = str(aadhaar) if aadhaar else None
        self.__otp_url = settings.NCODE['ekyc']['otp']['url']
        self.__otp_payload = self.__get_otp_payload()

    def __get_datetime_iso(self):
        return datetime.datetime.now().isoformat()

    def __get_transaction_id(self):
        return self.__aadhaar + "__upwards__" + self.__get_datetime_iso()

    def __get_otp_payload(self):
        return settings.NCODE['ekyc']['otp']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id())

    def generate_otp(self):
        otp_generation_successful = False
        if self.__aadhaar:
            response = requests.post(self.__otp_url, data=self.__otp_payload,
                                     headers={'Content-Type': 'application/xml'})
            otp_tree = ET.ElementTree(ET.fromstring(response.content))
            if otp_tree.getroot().attrib.get('status') in ['1', 1]:
                otp_generation_successful = True
        return otp_generation_successful
