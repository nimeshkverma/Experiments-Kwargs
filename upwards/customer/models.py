from __future__ import unicode_literals

from django.db import models

from common.models import ActiveModel, ActiveObjectManager, mobile_number_regex
from messenger.models import EmailVerification, PERSONAL


class Customer(ActiveModel):
    customer_id = models.AutoField(primary_key=True)
    altername_email_id = models.EmailField()
    is_altername_email_id_verified = models.BooleanField(default=False)
    altername_mob_no = models.CharField(max_length=12, validators=[
                                        mobile_number_regex], blank=True, default="")
    is_altername_mob_no_verified = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def validate_customer(self, customer_id):
        is_valid_customer = False
        if Customer.active_objects.get(pk=customer_id):
            is_valid_customer = True
        return is_valid_customer

    def save(self, *args, **kwargs):
        if not self.is_altername_email_id_verified:
            email_objects = EmailVerification.objects.filter(
                customer_id=self.customer_id, email_id=self.altername_email_id, email_type=PERSONAL)
            if email_objects:
                self.is_altername_email_id_verified = email_objects[
                    0].is_verified
        super(Customer, self).save(*args, **kwargs)

    @staticmethod
    def exists(customer_id):
        exists = False
        customer_objects = Customer.objects.filter(customer_id=customer_id)
        if customer_objects:
            exists = True
        return exists

    class Meta(object):
        db_table = "customer"

    def __unicode__(self):
        return "%s" % (str(self.customer_id))


class BankDetails(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=50, blank=False, null=False)
    account_number = models.CharField(max_length=20, blank=False, null=False)
    account_holder_name = models.CharField(
        max_length=50, blank=False, null=False)
    ifsc = models.CharField(max_length=20, blank=False, null=False)
    upi_mobile_number = models.CharField(max_length=12, validators=[
        mobile_number_regex], blank=True, default="")
    is_upi_mobile_number_verified = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_bank_details"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer_id), str(self.account_holder_name), str(self.bank_name))
