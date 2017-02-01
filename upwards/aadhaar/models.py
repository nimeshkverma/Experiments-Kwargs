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


class Aadhaar(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    aadhaar = models.CharField(max_length=12, validators=[
        aadhaar_regex], blank=True, null=False)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=True, null=False)
    last_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=True, null=False)
    father_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    father_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mother_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    mother_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default='')
    dob = models.DateField(blank=True, null=False)
    gender = models.CharField(
        max_length=1, default=MALE, choices=GENDER_CHOICES, blank=True, null=False)
    mobile_no = models.CharField(max_length=12, validators=[
                                 mobile_number_regex], blank=True, null=False)
    address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=False)
    address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=False)
    city = models.CharField(max_length=25, blank=True, null=False)
    state = models.CharField(max_length=25, blank=True, null=False)
    pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=False)
    pic_link = models.URLField(blank=True, null=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = 'customer_aadhaar'

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.aadhaar), str(self.first_name))
