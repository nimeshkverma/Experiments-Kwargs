try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import datetime
import requests
from cStringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.template.loader import get_template
from weasyprint import HTML
from documents.models import UPLOADED
from documents.serializers import DocumentsSerializer


class ESign(object):

    def __init__(self, aadhaar):
        self.__aadhaar = str(aadhaar) if aadhaar else None
        self.__otp_url = settings.NCODE['esign']['otp']['url']
        self.__otp_payload = self.__get_otp_payload()
        self.__sign_url = settings.NCODE['esign']['sign']['url']
        self.__sign_payload = {}

    def __get_datetime_iso(self):
        return datetime.datetime.now().isoformat()

    def __get_transaction_id(self):
        return self.__aadhaar + "__upwards__esign__" + self.__get_datetime_iso()

    def __get_otp_payload(self):
        return settings.NCODE['esign']['otp']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id())

    def __get_sign_payload(self, otp):
        return settings.NCODE['esign']['sign']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id(),
                                                                 otp=otp, pdf_path='/home/ncode_test', sign_pdf='/home/ncode_test/something.pdf', pdf_name='down.pdf')

    def __upload_documents(self, document_data):
        upload = False
        serializer = DocumentsSerializer(data=document_data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.check_table_conflict()
            serializer.save()
            print 9090
            upload = True
        print serializer.errors
        return upload

    def sign_document(self, otp):
        self.__sign_payload = self.__get_sign_payload(otp)
        print self.__sign_payload
        template = get_template('aadhaar/loan_agreement.html')
        html_part = template.render()
        pdf_file = HTML(string=html_part).write_pdf()
        buff = StringIO(pdf_file)
        buff.seek(0, 2)
        document = InMemoryUploadedFile(
            buff, 'file', 'xyz.pdf', None, buff.tell(), None)
        data = {
            'customer_id': 8,
            'document_type_id': 4,
            'status': UPLOADED,
            'document_1': document,
        }
        print self.__upload_documents(data)

        esign_successful = False
        # if self.__aadhaar:
        #     response = requests.post(self.__sign_url, data=self.__sign_payload,
        #                              headers={'Content-Type': 'application/xml'})
        #     print response.content
        #     otp_tree = ET.ElementTree(ET.fromstring(response.content))
        # if otp_tree.getroot().attrib.get('status') in ['1', 1]:
        #     otp_generation_successful = True
        return esign_successful
