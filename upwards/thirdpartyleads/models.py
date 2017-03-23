from __future__ import unicode_literals

from django.db import models

from common.models import (ActiveModel,
                           ActiveObjectManager,
                           numeric_regex,
                           alphabet_regex_allow_empty,
                           mobile_number_regex,
                           aadhaar_regex,
                           pan_regex,
                           pincode_regex,
                           GENDER_CHOICES,
                           YEAR_CHOICES,
                           MALE,)

RUBIQUE = 'rubique'
OTHERS = 'others'
LEAD_SOURCE_CHOICES = (
    (RUBIQUE, 'rubique'),
    (OTHERS, 'others'),
)

SALARIED = 'salaried'
SELF_EMPLOYED = 'self_employed'
OTHER = 'other'
EMPLOYEMENT_TYPE_CHOICES = (
    (SALARIED, 'salaried'),
    (SELF_EMPLOYED, 'self_employed'),
    (OTHERS, 'others'),
)

PRIVATE = 'private'
PROPRIETOR = 'proprietor'
GOVERNMENT = 'government'
OTHER = 'other'
EMPLOYER_TYPE_CHOICES = (
    (PRIVATE, 'private'),
    (PROPRIETOR, 'proprietor'),
    (GOVERNMENT, 'government'),
    (OTHER, 'other'),
)

DOCTOR = 'Doctor'
CHARTERED_ACCOUNTANT = 'Chatered Accountant'
COMPANY_SECRETARY = 'Company Secretary'
CONSULTANT = 'Consultant'
ARCHITECT = 'Architect'
LAWYER = 'Lawyer'
TEACHER = 'Teacher'
OTHER_PROFESSION_TYPE = 'Other'
PROFESSION_TYPE_CHOICES = (
    (DOCTOR, 'Doctor'),
    (CHARTERED_ACCOUNTANT, 'Chatered Accountant'),
    (COMPANY_SECRETARY, 'Company Secretary'),
    (CONSULTANT, 'Consultant'),
    (ARCHITECT, 'Architect'),
    (LAWYER, 'Lawyer'),
    (TEACHER, 'Teacher'),
    (OTHER_PROFESSION_TYPE, 'Other'),
)

BANK_TRANSFER = 'Bank account transfer'
CHEQUE = 'Cheque payment'
CASH = 'Cash payment'
SALARY_MODE_CHOICES = (
    (BANK_TRANSFER, 'Bank account transfer'),
    (CHEQUE, 'Cheque payment'),
    (CASH, 'Cash payment'),
)

OWNED = 'Owned'
RENTED = 'Rented'
COMPANY_PROVIDED = 'Company Provided'
PAYING_GUEST = 'Paying Guest'
ANCESTRAL_PROPERTY = 'Ancestral Property'
RESICUM_OFFICE = 'Resicum Office'
ACCOMMODATION_TYPE_CHOICES = (
    (OWNED, 'Owned'),
    (RENTED, 'Rented'),
    (COMPANY_PROVIDED, 'Company Provided'),
    (PAYING_GUEST, 'Paying Guest'),
    (ANCESTRAL_PROPERTY, 'Ancestral Property'),
    (RESICUM_OFFICE, 'Resicum Office'),
)


class ThirdPartyLead(ActiveModel):
    third_party_lead_id = models.AutoField(primary_key=True)
    lead_source = models.CharField(
        max_length=50, default=RUBIQUE, choices=LEAD_SOURCE_CHOICES)
    leads_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=False, null=False)
    leads_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=False, null=False)
    gender = models.CharField(
        max_length=50, default=MALE, choices=GENDER_CHOICES, blank=False, null=False)
    fathers_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=False, null=False)
    fathers_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mothers_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mothers_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    dob = models.DateField(blank=False, null=False)
    current_address_line1 = models.CharField(
        max_length=256, blank=False, null=False)
    current_address_line2 = models.CharField(
        max_length=256, blank=False, null=False)
    current_city = models.CharField(max_length=25, blank=False, null=False)
    current_state = models.CharField(max_length=25, blank=False, null=False)
    current_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=False, null=False)
    permanent_address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_city = models.CharField(
        max_length=25, blank=True, null=True, default="")
    permanent_state = models.CharField(
        max_length=25, blank=True, null=True, default="")
    permanent_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=True, default="")
    aadhaar = models.CharField(max_length=12, validators=[
        aadhaar_regex], blank=False, null=False)
    aadhaar_mob_no = models.CharField(max_length=12, validators=[
        mobile_number_regex], blank=True, default="")
    alternate_mob_no = models.CharField(max_length=12, validators=[
                                        mobile_number_regex], blank=True, default="")
    landline_no_office = models.CharField(
        max_length=12, validators=[numeric_regex], blank=False, null=False)
    landline_no_residence = models.CharField(
        max_length=12, validators=[numeric_regex], blank=False, null=False)
    personal_email = models.EmailField(blank=False, null=False)
    pan = models.CharField(max_length=10, validators=[
                           pan_regex], blank=False, null=False)
    employement_type = models.CharField(
        max_length=50, blank=False, null=False, choices=EMPLOYEMENT_TYPE_CHOICES)
    employer = models.CharField(max_length=256, blank=False, null=False)
    employer_type = models.CharField(
        max_length=50, blank=False, null=False, choices=EMPLOYER_TYPE_CHOICES)
    profession_type = models.CharField(
        max_length=50, blank=False, null=False, choices=PROFESSION_TYPE_CHOICES)
    designation = models.CharField(
        max_length=50, blank=False, null=False)
    company_email = models.EmailField(blank=True, null=True)
    department = models.CharField(
        max_length=50, blank=True, null=True, default="")
    monthly_salary = models.IntegerField(blank=False, null=False)
    office_city = models.CharField(
        max_length=50, blank=False, null=False)
    current_company_experience = models.IntegerField(blank=False, null=False)
    total_experience = models.IntegerField(blank=False, null=False)
    highest_qualification = models.CharField(
        max_length=25, blank=True, null=True)
    highest_qualification_completion_year = models.IntegerField(
        choices=YEAR_CHOICES, blank=True, null=True)
    highest_qualification_college = models.CharField(
        max_length=256, blank=True, default="")
    active_loans = models.IntegerField(blank=True, null=True, default=0)
    primary_bank_account_number = models.CharField(
        max_length=20, blank=True, null=True, default="")
    primary_bank_account_holder_name = models.CharField(
        max_length=50, blank=True, null=True, default="")
    primary_bank_name = models.CharField(
        max_length=256, blank=False, null=False)
    primary_bank_ifsc = models.CharField(
        max_length=20, blank=True, null=True, default="")
    cheque_bounced_3 = models.BooleanField(blank=False, null=False)
    exsisting_loans = models.BooleanField(blank=False, null=False)
    accommodation_type = models.CharField(
        max_length=50, blank=False, null=False, choices=ACCOMMODATION_TYPE_CHOICES)
    mode_of_salary = models.CharField(
        max_length=50, blank=False, null=False, choices=SALARY_MODE_CHOICES)
    current_residence_years = models.IntegerField(
        blank=True, null=True, default=0)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "third_party_lead"

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.third_party_lead_id), str(self.lead_source), str(self.leads_first_name))

UPLOADED = 'uploaded'
VERIFIED = 'verified'

DOCUMENT_STATUS_CHOICES = (
    (UPLOADED, 'uploaded'),
    (VERIFIED, 'verified'),
)


AADHAAR = 'aadhaar'
PAN = 'pan'
CURRENT_ADDRESS_PROOF = 'current_address_proof'
INCOME_PROOF = 'income_proof'
BANK_STATEMENT = 'bank_statement'
PASSPORT_PIC = 'passport_pic'

DOCUMENT_TYPE_CHOICES = (
    (AADHAAR, 'aadhaar'),
    (PAN, 'pan'),
    (CURRENT_ADDRESS_PROOF, 'current_address_proof'),
    (INCOME_PROOF, 'income_proof'),
    (BANK_STATEMENT, 'bank_statement'),
    (PASSPORT_PIC, 'passport_pic'),
)


def content_file_name(instance, filename):
    return "thirdparty/{lead_source}/{lead_id}/{filename}".format(lead_source=str(instance.third_party_lead.lead_source), lead_id=str(instance.third_party_lead_id), filename=filename)


class ThirdPartyLeadDocuments(ActiveModel):
    third_party_lead = models.ForeignKey(
        'ThirdPartyLead', on_delete=models.CASCADE)
    document_type = models.CharField(
        max_length=50, default=AADHAAR, choices=DOCUMENT_TYPE_CHOICES)
    document_1 = models.FileField(upload_to=content_file_name)
    document_2 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_3 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_4 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_5 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_6 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    status = models.CharField(
        max_length=50, default=UPLOADED, choices=DOCUMENT_STATUS_CHOICES)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = 'third_party_lead_documents'
        unique_together = ('third_party_lead', 'document_type')

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.third_party_lead), str(self.document_type), str(self.status))
