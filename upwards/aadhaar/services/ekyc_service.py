try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from django.core.files.uploadedfile import InMemoryUploadedFile
from cStringIO import StringIO
import datetime
import requests
from django.conf import settings
from common.models import MALE, FEMALE, OTHER
from aadhaar.models import Aadhaar
from documents.models import UPLOADED
from documents.serializers import DocumentsSerializer


GENDER_MAP = {
    'M': MALE,
    'F': FEMALE,
    'T': OTHER
}


class EKYC(object):

    def __init__(self, aadhaar):
        self.__aadhaar = str(aadhaar) if aadhaar else None
        self.__otp_url = settings.NCODE['ekyc']['otp']['url']
        self.__otp_payload = self.__get_otp_payload()
        self.__kyc_url = settings.NCODE['ekyc']['kyc']['url']
        self.__kyc_payload = None
        self.__kyc_data = {}

    def __get_datetime_iso(self):
        return datetime.datetime.now().isoformat()

    def __get_transaction_id(self):
        return self.__aadhaar + "__upwards__ekyc__" + self.__get_datetime_iso()

    def __get_otp_payload(self):
        return settings.NCODE['ekyc']['otp']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id())

    def __get_kyc_payload(self, otp):
        return settings.NCODE['ekyc']['kyc']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id(), otp=otp)

    def generate_otp(self):
        otp_generation_successful = False
        if self.__aadhaar:
            response = requests.post(self.__otp_url, data=self.__otp_payload,
                                     headers={'Content-Type': 'application/xml'})
            otp_tree = ET.ElementTree(ET.fromstring(response.content))
            if otp_tree.getroot().attrib.get('status') in ['1', 1]:
                otp_generation_successful = True
        return otp_generation_successful

    def get_kyc_data(self, otp):
        self.__kyc_payload = self.__get_kyc_payload(otp)
        if self.__aadhaar and otp:
            try:
                response = requests.post(self.__kyc_url, data=self.__kyc_payload, headers={
                    'Content-Type': 'application/xml'})
                aadhaar_data_node = ET.ElementTree(ET.fromstring(ET.ElementTree(ET.fromstring(ET.ElementTree(ET.fromstring(response.text)).getroot(
                ).find('EkycResp').text.decode('base64'))).getroot().find('KycRes').text.decode('base64'))).getroot().find('UidData')
                self.__kyc_data = {
                    'profile_pic': aadhaar_data_node.find('Pht').text,
                    'aadhaar_card': aadhaar_data_node.find('Prn').text,
                    'proof_of_identity': aadhaar_data_node.find('Poi').attrib,
                    'proof_of_address': aadhaar_data_node.find('Poa').attrib,
                }
            except Exception as e:
                pass

    def __get_proccessed_poi(self):
        data = {}
        poi = self.__kyc_data.get('proof_of_identity')
        if poi:
            if poi.get('name'):
                name_list = str(poi.get('name')).split(' ')
                if name_list:
                    data['first_name'] = name_list[0]
                    data['last_name'] = ' '.join(name_list[1:])
            if poi.get('phone'):
                data['mobile_no'] = poi['phone']
            if poi.get('gender') and GENDER_MAP.get(poi['gender']):
                data['gender'] = GENDER_MAP[poi['gender']]
            if poi.get('dob'):
                data['dob'] = '-'.join(poi['dob'].split('-')[::-1])
        return data

    def __get_proccessed_poa(self):
        data = {}
        poa = self.__kyc_data.get('proof_of_address')
        if poa:
            if poa.get('co'):
                name_list = str(poa.get('co')).split(' ')
                if name_list:
                    data['father_first_name'] = ' '.join(name_list[:2])
                    data['father_last_name'] = ' '.join(name_list[2:])
            if poa.get('pc'):
                data['pincode'] = poa['pc']
            if poa.get('house'):
                data['address_line1'] = poa['house']
            if poa.get('loc'):
                data['address_line2'] = poa['loc'] + ' ' + poa.get('dist', '')
            if poa.get('state'):
                data['state'] = poa['state']
            if poa.get('vtc'):
                data['city'] = poa['vtc']
            if poa.get('dob'):
                data['dob'] = '-'.join(poa['dob'].split('-')[::-1])
        return data

    def update_aadhaar_table(self, customer_id):
        aadhaar_detail_data = self.__get_proccessed_poi()
        aadhaar_detail_data.update(self.__get_proccessed_poa())
        Aadhaar.objects.filter(aadhaar=self.__aadhaar, customer_id=customer_id).update(
            **aadhaar_detail_data)

    def __upload_documents(self, document_data):
        upload = False
        serializer = DocumentsSerializer(data=document_data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.check_table_conflict()
            serializer.save()
            upload = True
        return upload

    def upload_document(self, customer_id):
        document_map = {
            'profile_pic': {
                'name': '_profilepic1.jpg',
                'document_type_id': '1'},
            'aadhaar_card': {
                'name': '_aadhaar1.pdf',
                'document_type_id': '2'},
        }
        for document_key, document_value in document_map.iteritems():
            document_decoded = self.__kyc_data.get(
                document_key, '').decode('base64')
            if document_decoded:
                document_file_name = 'customer' + \
                    str(customer_id) + document_value['name']
                buff = StringIO(document_decoded)
                buff.seek(0, 2)
                document = InMemoryUploadedFile(
                    buff, 'file', document_file_name, None, buff.tell(), None)
                data = {
                    'customer_id': str(customer_id),
                    'document_type_id': document_value['document_type_id'],
                    'status': UPLOADED,
                    'document_1': document,
                }
                self.__upload_documents(data)
