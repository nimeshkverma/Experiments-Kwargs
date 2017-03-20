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


class ThirdPartyLead(ActiveModel):
    third_party_lead_id = models.AutoField(primary_key=True)
    lead_source = models.CharField(
        max_length=50, default=RUBIQUE, choices=LEAD_SOURCE_CHOICES)
    gender = models.CharField(
        max_length=50, default=MALE, choices=GENDER_CHOICES)
    leads_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    leads_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    aadhaar = aadhaar = models.CharField(max_length=12, validators=[
                                         aadhaar_regex], blank=True, null=True)
    fathers_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    fathers_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mothers_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mothers_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    dob = models.DateField(blank=True, null=True)
    permanent_address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_city = models.CharField(max_length=25, blank=True, null=True)
    permanent_state = models.CharField(max_length=25, blank=True, null=True)
    permanent_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=True)
    current_address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    current_address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    current_city = models.CharField(max_length=25, blank=True, null=True)
    current_state = models.CharField(max_length=25, blank=True, null=True)
    current_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=True)
    aadhaar_mob_no = models.CharField(max_length=12, validators=[
        mobile_number_regex], blank=True, default="")
    alternate_mob_no = models.CharField(max_length=12, validators=[
                                        mobile_number_regex], blank=True, default="")
    landline_no_office = models.CharField(
        max_length=12, validators=[numeric_regex], blank=True, default="")
    landline_no_residence = models.CharField(
        max_length=12, validators=[numeric_regex], blank=True, default="")
    personal_email_id = models.EmailField(blank=True, null=True)
    pan = models.CharField(max_length=10, validators=[
                           pan_regex], blank=True, null=True)
    employement_type = models.CharField(
        max_length=50, default=SALARIED, choices=EMPLOYEMENT_TYPE_CHOICES)
    employer = models.CharField(max_length=256, blank=True, default="")
    employer_type = models.CharField(
        max_length=50, default=PRIVATE, choices=EMPLOYER_TYPE_CHOICES)
    company_email = models.EmailField(blank=True, null=True)
    department = models.CharField(
        max_length=50, blank=True, null=True, default="")
    designation = models.CharField(
        max_length=50, blank=True, null=True, default="")
    monthly_salary = models.IntegerField(blank=True, null=True)
    office_city = models.CharField(
        max_length=50, blank=True, null=True, default="")
    current_company_experience = models.IntegerField(
        blank=True, null=True, default=0)
    total_experience = models.IntegerField(blank=True, null=True, default=0)
    highest_qualification = models.CharField(
        max_length=25, blank=True, null=True)
    completion_year = models.IntegerField(
        choices=YEAR_CHOICES, blank=True, null=True)
    highest_qualification_college = models.CharField(
        max_length=256, blank=True, default="")
    active_loans = models.IntegerField(blank=True, null=True, default=0)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_holder_name = models.CharField(
        max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=256, blank=True, null=True)
    ifsc = models.CharField(max_length=20, blank=True, null=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "third_party_lead"

    def __unicode__(self):
        return "%s" % (str(self.customer_id))


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
