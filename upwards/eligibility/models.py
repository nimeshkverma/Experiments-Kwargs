from __future__ import unicode_literals

from django.db import models

from common.models import ActiveModel, ActiveObjectManager


class Finance(ActiveModel):
    customer = models.ForeignKey(
        'customer.Customer', on_delete=models.CASCADE)
    any_active_loans = models.BooleanField(default=False)
    any_owned_vehicles = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_finance"

    def __unicode__(self):
        return "%s__any_active_loans:%s__any_owned_vehicles:%s" % (str(self.customer), str(self.any_active_loans), str(self.any_owned_vehicles))
