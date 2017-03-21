import datetime
from eligibility.models import Education, Profession
from customer.models import BankDetails
from pan.models import Pan
from aadhaar.models import Aadhaar
from participant.models import Borrower


class LoanAgreement(object):

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.data = self.__data()

    def __get_full_name(self, first_name, last_name):
        return (first_name if first_name else '') + ' ' + (last_name if last_name else '')

    def __get_aadhaar_data(self):
        aadhaar_data = {}
        aadhaar_object = Aadhaar.objects.get(customer_id=self.customer_id)
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
            'address_line_1'] = aadhaar_object.permanent_address_line1.title() if aadhaar_object.permanent_address_line1 else ''
        aadhaar_data[
            'address_line_2'] = aadhaar_object.permanent_address_line2 .title()if aadhaar_object.permanent_address_line2 else ''
        aadhaar_data[
            'city'] = aadhaar_object.permanent_city.title() if aadhaar_object.permanent_city else ''
        aadhaar_data[
            'state'] = aadhaar_object.permanent_state.title() if aadhaar_object.permanent_state else ''
        aadhaar_data[
            'pincode'] = aadhaar_object.permanent_pincode if aadhaar_object.permanent_pincode else ''
        aadhaar_data[
            'aadhaar_mob_no'] = str(aadhaar_object.mobile_no) if aadhaar_object.mobile_no else ''
        aadhaar_data['age'] = self.__age(aadhaar_object.dob)
        return aadhaar_data

    def __eligibility_data(self):
        eligibility_data = {}
        education_object = Education.objects.get(customer_id=self.customer_id)
        profession_object = Profession.objects.get(
            customer_id=self.customer_id)
        borrower_object = Borrower.objects.get(customer_id=self.customer_id)
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

    def __get_other_data(self):
        data = {}
        pan_object = Pan.objects.get(customer_id=self.customer_id)
        data['present_date'] = datetime.datetime.now().strftime("%d-%m-%Y")
        data['pan'] = pan_object.pan if pan_object.pan else ''
        data['email_id'] = pan_object.customer.alternate_email_id if pan_object.customer.alternate_email_id else ''
        data['alternate_mob_no'] = pan_object.customer.alternate_mob_no if pan_object.customer.alternate_mob_no else ''
        return data

    def __get_bank_data(self):
        data = {
            'bank': " ____________________<to be filled later based on user provided>",
            'ifsc': " ______________________<to be filled later based on user provided>"
        }
        # bank_object = BankDetails.objects.get(customer_id=self.customer_id)
        # data['bank'] = bank_object.bank_name.title(
        # ) if bank_object.bank_name else ''
        # data['ifsc'] = bank_object.ifsc if bank_object.ifsc else ''
        return data

    def __age(self, when, on=None):
        if on is None:
            on = datetime.date.today()
        was_earlier = (on.month, on.day) < (when.month, when.day)
        return on.year - when.year - (was_earlier)

    def __data(self):
        data = self.__get_aadhaar_data()
        data.update(self.__eligibility_data())
        data.update(self.__get_bank_data())
        data.update(self.__get_other_data())
        return data
