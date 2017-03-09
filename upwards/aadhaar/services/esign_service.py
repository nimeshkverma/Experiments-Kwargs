try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import datetime
import subprocess
import requests
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.template.loader import get_template
from documents.models import UPLOADED
from documents.serializers import DocumentsSerializer
from esign_constants import SIGN_DOCUMENT_COMMANDS, UNSIGNED_PDF_PATH, UNSIGNED_PDF_NAME, PDF_DIRECTORY, SIGNED_PDF_PATH, SIGNED_PDF_PAYLOAD_PATH, PDF_PAYLOAD_DIRECTORY


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

    def __get_sign_payload(self, otp, pdf_path, pdf_name, sign_pdf):
        return settings.NCODE['esign']['sign']['payload'].format(uid=self.__aadhaar, ts=self.__get_datetime_iso(), txn=self.__get_transaction_id(),
                                                                 otp=otp, pdf_path=pdf_path, sign_pdf=sign_pdf, pdf_name=pdf_name)

    def __upload_documents(self, document_data):
        upload = False
        serializer = DocumentsSerializer(data=document_data)
        if serializer.is_valid():
            serializer.validate_foreign_keys()
            serializer.check_table_conflict()
            serializer.save()
            upload = True
        return upload

    def __get_file_name(self, customer_id, signed=False):
        last_name_part = '_signed_loan_agreement.pdf' if signed else '_unsigned_loan_agreement.pdf'
        return 'customer' + str(customer_id) + last_name_part

    def __s3_loan_agreement_url(self, customer_id, signed=False):
        return settings.S3_URL + str(customer_id) + '/' + self.__get_file_name(customer_id, signed)

    def __upload_loan_agreement(self, customer_id, signed=False):
        pdf = open(SIGNED_PDF_PATH.format(customer_id=customer_id), 'rb') if signed else open(
            UNSIGNED_PDF_PATH.format(customer_id=customer_id), 'rb')
        pdf.seek(0)
        buff = StringIO.StringIO(pdf.read())
        document = InMemoryUploadedFile(
            buff, 'file', self.__get_file_name(customer_id, signed), None, buff, None)
        data = {
            'customer_id': customer_id,
            'document_type_id': 7 if signed else 6,
            'status': UPLOADED,
            'document_1': document,
        }
        return self.__upload_documents(data)

    def generate_and_sign_aggrement(self, otp, customer_id):
        response = {
            'loan_agreement_url': None,
            'unsigned_loan_agreement_uploaded': False,
            'esigned_process_completed': False,
            'signed_loan_agreement_uploaded': False
        }
        for command_key in ['new_directory', 'change_directory_mode', 'make_unsigned_pdf', 'change_pdf_mode']:
            command_key, SIGN_DOCUMENT_COMMANDS[
                command_key].format(customer_id=customer_id)
            subprocess.call(SIGN_DOCUMENT_COMMANDS[command_key].format(
                customer_id=customer_id), shell=True)
        response[
            'unsigned_loan_agreement_uploaded'] = self.__upload_loan_agreement(customer_id)
        response['loan_agreement_url'] = self.__s3_loan_agreement_url(
            customer_id)
        if self.__sign_document(otp, customer_id):
            response['esigned_process_completed'] = True
            response['signed_loan_agreement_uploaded'] = self.__upload_loan_agreement(
                customer_id, True)
            response['loan_agreement_url'] = self.__s3_loan_agreement_url(
                customer_id, True)
        subprocess.call(SIGN_DOCUMENT_COMMANDS['delete_directory'].format(
            customer_id=customer_id), shell=True)
        return response

    def __sign_document(self, otp, customer_id):
        sign_generation_successful = False
        pdf_path = PDF_PAYLOAD_DIRECTORY.format(customer_id=customer_id)
        pdf_name = UNSIGNED_PDF_NAME.format(customer_id=customer_id)
        sign_pdf = SIGNED_PDF_PAYLOAD_PATH.format(customer_id=customer_id)
        print pdf_path, pdf_name, sign_pdf
        self.__sign_payload = self.__get_sign_payload(
            otp, pdf_path, pdf_name, sign_pdf)
        if self.__aadhaar:
            response = requests.post(self.__sign_url, data=self.__sign_payload,
                                     headers={'Content-Type': 'application/xml'})
            sign_tree = ET.ElementTree(ET.fromstring(response.content))
            print response.content
        if sign_tree.getroot().attrib.get('status') in ['1', 1]:
            sign_generation_successful = True
        return sign_generation_successful

    def generate_otp(self):
        otp_generation_successful = False
        if self.__aadhaar:
            response = requests.post(self.__otp_url, data=self.__otp_payload,
                                     headers={'Content-Type': 'application/xml'})
            otp_tree = ET.ElementTree(ET.fromstring(response.content))
            if otp_tree.getroot().attrib.get('status') in ['1', 1]:
                otp_generation_successful = True
        return otp_generation_successful
