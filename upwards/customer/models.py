from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save

from common.models import ActiveModel, ActiveObjectManager, mobile_number_regex, pincode_regex
from messenger.models import EmailVerification, PERSONAL
from activity.models import register_customer_state
from activity.model_constants import BANK_DETAIL_SUBMIT


class Customer(ActiveModel):
    customer_id = models.AutoField(primary_key=True)
    alternate_email_id = models.EmailField()
    is_alternate_email_id_verified = models.BooleanField(default=False)
    alternate_mob_no = models.CharField(max_length=12, validators=[
                                        mobile_number_regex], blank=True, default="")
    is_alternate_mob_no_verified = models.BooleanField(default=False)
    current_address_line1 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    current_address_line2 = models.CharField(
        max_length=256, default='', blank=True, null=True)
    current_city = models.CharField(max_length=25, blank=True, null=True)
    current_state = models.CharField(max_length=25, blank=True, null=True)
    current_pincode = models.CharField(max_length=6, validators=[
        pincode_regex], blank=True, null=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def validate_customer(self, customer_id):
        is_valid_customer = False
        if Customer.active_objects.get(pk=customer_id):
            is_valid_customer = True
        return is_valid_customer

    def save(self, *args, **kwargs):
        if not self.is_alternate_email_id_verified:
            email_objects = EmailVerification.objects.filter(
                customer_id=self.customer_id, email_id=self.alternate_email_id, email_type=PERSONAL)
            if email_objects:
                self.is_alternate_email_id_verified = email_objects[
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
    branch_detail = models.CharField(max_length=256, blank=False, null=False)
    ifsc = models.CharField(max_length=20, blank=False, null=False)
    upi_mobile_number = models.CharField(max_length=12, validators=[
        mobile_number_regex], blank=True, default="")
    is_upi_mobile_number_verified = models.BooleanField(default=False)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    @staticmethod
    def register_bank_submit_customer_state(sender, instance, created, **kwargs):
        if created:
            register_customer_state(
                BANK_DETAIL_SUBMIT, instance.customer_id)

    class Meta(object):
        db_table = "customer_bank_details"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer_id), str(self.account_holder_name), str(self.bank_name))

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.company), str(self.salary))

post_save.connect(
    BankDetails.register_bank_submit_customer_state, sender=BankDetails)
