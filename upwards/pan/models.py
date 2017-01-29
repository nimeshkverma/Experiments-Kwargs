from __future__ import unicode_literals

from django.db import models

from common.models import (	ActiveModel,
                            ActiveObjectManager,
                            pan_regex,
                            alphabet_regex,
                            alphabet_regex_allow_empty,
                            alphabet_whitespace_regex,)


class Pan(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    pan = models.CharField(max_length=10, validators=[
        pan_regex], blank=False, null=False)
    is_verified = models.BooleanField(default=False)
    title = models.CharField(max_length=10, validators=[
        alphabet_regex_allow_empty], default="")
    first_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=False, null=False)
    middle_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    last_name = models.CharField(max_length=25, validators=[
        alphabet_whitespace_regex], blank=False, null=False)
    father_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    father_middle_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    father_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], default="")
    dob = models.DateField()
    status = models.CharField(max_length=25, default="")
    pan_updates = models.IntegerField(default=1)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_pan"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.pan), str(self.first_name))
