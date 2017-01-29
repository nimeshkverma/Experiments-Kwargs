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


class Aadhaar(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    aadhaar = models.CharField(max_length=12, validators=[
        aadhaar_regex], blank=False, null=False)
    is_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=False, null=False)
    last_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=False, null=False)
    father_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    father_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    mother_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    mother_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    dob = models.DateField()
    gender = models.CharField(
        max_length=1, default=MALE, choices=GENDER_CHOICES)
    mobile_no = models.CharField(max_length=12, validators=[
                                 mobile_number_regex], blank=False, null=False)
    address_line1 = models.CharField(max_length=256, default="")
    address_line2 = models.CharField(max_length=256, default="")
    city = models.CharField(max_length=25, blank=False, null=False)
    state = models.CharField(max_length=25, blank=False, null=False)
    pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=False, null=False)
    pic_link = models.FileField()
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_aadhaar"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.aadhaar), str(self.first_name))
