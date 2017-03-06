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
# from weasyprint import HTML, CSS
from documents.models import UPLOADED
from documents.serializers import DocumentsSerializer
from eligibility.models import Education, Profession
from customer.models import BankDetails
from pan.models import Pan
from aadhaar.models import Aadhaar
from participant.models import Borrower


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

    def __get_full_name(self, first_name, last_name):
        return (first_name if first_name else '') + ' ' + (last_name if last_name else '')

    def __get_aadhaar_data(self, customer_id):
        aadhaar_data = {}
        aadhaar_object = Aadhaar.objects.get(customer_id=customer_id)
        aadhaar_data['borrower_full_name'] = self.__get_full_name(
            aadhaar_object.first_name, aadhaar_object.last_name).title()
        aadhaar_data[
            'aadhaar'] = aadhaar_object.aadhaar.title() if aadhaar_object.aadhaar else ''
        aadhaar_data[
            'gender'] = aadhaar_object.gender.title() if aadhaar_object.gender else ''
        aadhaar_data['dob'] = aadhaar_object.dob.strftime(
            "%d-%m-%Y") if aadhaar_object.dob else ''
        aadhaar_data['fathers_full_name'] = self.__get_full_name(
            aadhaar_object.father_first_name, aadhaar_object.father_last_name).title()
        aadhaar_data['mothers_full_name'] = self.__get_full_name(
            aadhaar_object.mother_first_name, aadhaar_object.mother_first_name).title()
        aadhaar_data[
            'address_line_1'] = aadhaar_object.address_line1.title() if aadhaar_object.address_line1 else ''
        aadhaar_data[
            'address_line_2'] = aadhaar_object.address_line2 .title()if aadhaar_object.address_line2 else ''
        aadhaar_data[
            'city'] = aadhaar_object.city.title() if aadhaar_object.city else ''
        aadhaar_data[
            'state'] = aadhaar_object.state.title() if aadhaar_object.state else ''
        aadhaar_data[
            'pincode'] = aadhaar_object.pincode if aadhaar_object.pincode else ''
        aadhaar_data[
            'aadhaar_mob_no'] = str(aadhaar_object.mobile_no) if aadhaar_object.mobile_no else ''
        aadhaar_data['age'] = self.__age(aadhaar_object.dob)
        return aadhaar_data

    def __eligibility_data(self, customer_id):
        eligibility_data = {}
        education_object = Education.objects.get(customer_id=customer_id)
        profession_object = Profession.objects.get(customer_id=customer_id)
        borrower_object = Borrower.objects.get(customer_id=customer_id)
        eligibility_data[
            'qualification'] = education_object.qualification.title() if education_object.qualification else ''
        eligibility_data[
            'company'] = profession_object.company.name.title() if profession_object.company.name else ''
        eligibility_data[
            'company_type'] = profession_object.organisation_type.name.title() if profession_object.organisation_type.name else ''
        eligibility_data[
            'occupation'] = 'Salaried'
        eligibility_data['salary'] = str(
            profession_object.salary) if profession_object.salary else ''
        eligibility_data[
            'eligibility_amount'] = str(borrower_object.credit_limit) if borrower_object.credit_limit else ''

        return eligibility_data

    def __get_other_data(self, customer_id):
        data = {}
        pan_object = Pan.objects.get(customer_id=customer_id)
        bank_object = BankDetails.objects.get(customer_id=customer_id)
        data['present_date'] = datetime.datetime.now().strftime("%d-%m-%Y")
        data['pan'] = pan_object.pan if pan_object.pan else ''
        data['email_id'] = pan_object.customer.alternate_email_id if pan_object.customer.alternate_email_id else ''
        data['bank'] = bank_object.bank_name.title(
        ) if bank_object.bank_name else ''
        data['ifsc'] = bank_object.ifsc if bank_object.ifsc else ''
        data['alternate_mob_no'] = pan_object.customer.alternate_mob_no if pan_object.customer.alternate_mob_no else ''
        return data

    def __age(self, when, on=None):
        if on is None:
            on = datetime.date.today()
        was_earlier = (on.month, on.day) < (when.month, when.day)
        return on.year - when.year - (was_earlier)

    def __pdf_html(self, customer_id):
        context = self.__get_aadhaar_data(customer_id)
        context.update(self.__eligibility_data(customer_id))
        context.update(self.__get_other_data(customer_id))

        template = get_template('aadhaar/loan_agreement2.html')
        html_part = template.render(context)
        print html_part
        return html_part

    def sign_document(self, otp, customer_id):
        self.__sign_payload = self.__get_sign_payload(otp)
        print self.__sign_payload
        # pdf_file = HTML(string=self.__pdf_html(customer_id)).write_pdf()
        # pdf_file = HTML(
        #     'https://s3-us-west-2.amazonaws.com/kycdocument/8/Loan+Agreement.html').write_pdf()
        # buff = StringIO(pdf_file)
        # buff.seek(0, 2)
        # document = InMemoryUploadedFile(
        #     buff, 'file', 'xyzwqw.pdf', None, buff.tell(), None)
        # data = {
        #     'customer_id': 9,
        #     'document_type_id': 5,
        #     'status': UPLOADED,
        #     'document_1': document,
        # }
        # print self.__upload_documents(data)

        esign_successful = False
        # if self.__aadhaar:
        #     response = requests.post(self.__sign_url, data=self.__sign_payload,
        #                              headers={'Content-Type': 'application/xml'})
        #     print response.content
        #     otp_tree = ET.ElementTree(ET.fromstring(response.content))
        # if otp_tree.getroot().attrib.get('status') in ['1', 1]:
        #     otp_generation_successful = True
        return esign_successful
