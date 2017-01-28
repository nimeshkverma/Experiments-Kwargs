from __future__ import unicode_literals

from django.db import models

from common.models import ActiveModel, ActiveObjectManager, mobile_number_regex


class Customer(ActiveModel):
    customer_id = models.AutoField(primary_key=True)
    altername_email_id = models.EmailField()
    is_altername_email_id_verified = models.BooleanField(default=False)
    altername_mob_no = models.CharField(max_length=12, validators=[
                                        mobile_number_regex], blank=True, default="")
    is_altername_mob_no_verified = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer"

    def __unicode__(self):
        return "%s" % (str(self.id))
