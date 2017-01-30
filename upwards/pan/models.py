from __future__ import unicode_literals

from django.db import models

from common.models import (	ActiveModel,
                            ActiveObjectManager,
                            pan_regex,
                            alphabet_regex_allow_empty,)


class Pan(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    pan = models.CharField(max_length=10, validators=[
        pan_regex], blank=False, null=False)
    is_verified = models.BooleanField(blank=True, default=False)
    title = models.CharField(max_length=10, validators=[
        alphabet_regex_allow_empty], blank=True, default="")
    first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, null=False, default="")
    middle_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default="")
    last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, null=False, default="")
    father_first_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default="")
    father_middle_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default="")
    father_last_name = models.CharField(max_length=25, validators=[
        alphabet_regex_allow_empty], blank=True, default="")
    dob = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=25, blank=True, default="")
    pan_updates = models.IntegerField(blank=True, default=1)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_pan"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.pan), str(self.first_name))
