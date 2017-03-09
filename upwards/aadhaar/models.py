from __future__ import unicode_literals

from django.db import models

from common.models import (	ActiveModel,
                            ActiveObjectManager,
                            aadhaar_regex,
                            alphabet_regex,
                            alphabet_regex_allow_empty,
                            alphabet_whitespace_regex,
                            mobile_number_regex,
                            pincode_regex,
                            GENDER_CHOICES,
                            MALE,)
from common.exceptions import NotAcceptableError, ConflictError

EKYC = 'ekyc'
UPWARDS = 'upwards'

AADHAAR_DATA_SOURCE_CHOICES = (
    (EKYC, 'EKYC'),
    (UPWARDS, 'Upwards'),
)


class Aadhaar(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    aadhaar = aadhaar = models.CharField(max_length=12, validators=[
                                         aadhaar_regex], blank=True, null=False)
    aadhaar_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=True, null=True)
    first_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    last_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=True, null=True)
    last_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    father_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    father_first_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    father_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    father_last_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    mother_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mother_first_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    mother_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mother_last_name_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    dob = models.DateField(blank=True, null=True)
    dob_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    gender = models.CharField(
        max_length=1, default=MALE, choices=GENDER_CHOICES, blank=True, null=True)
    gender_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    mobile_no = models.CharField(max_length=12, validators=[
                                 mobile_number_regex], blank=True, null=False)
    mobile_no_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    permanent_address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_address_line1_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    permanent_address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    permanent_address_line2_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    permanent_city = models.CharField(max_length=25, blank=True, null=True)
    permanent_city_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    permanent_state = models.CharField(max_length=25, blank=True, null=True)
    permanent_state_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    permanent_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=True)
    permanent_pincode_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    pic_link = models.URLField(blank=True, null=True)
    pic_link_source = models.CharField(
        max_length=25, default=UPWARDS, choices=AADHAAR_DATA_SOURCE_CHOICES, blank=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = 'customer_aadhaar'

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.aadhaar), str(self.first_name))
