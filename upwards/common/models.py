from __future__ import unicode_literals
from datetime import datetime
from django.core.validators import RegexValidator
from django.db import models

mobile_number_regex = RegexValidator(
    regex=r'^$|\d{10}$', message="Mobile number must be entered in the format: '9999999999'. 10 digits allowed.")
pan_regex = RegexValidator(
    regex=r'[A-Z]{5}\d{4}[A-Z]{1}', message="PAN must be entered in the format: 'ABCDE1234F'. 10 Characters allowed.")
aadhaar_regex = RegexValidator(
    regex=r'^$\d{12}$', message="AADHAAR must be entered in the format: '123456789123'. 12 digits allowed.")
alphabet_regex = RegexValidator(
    regex=r'[a-zA-Z]+', message="Data must be entered in Alphabets only.")
alphabet_regex_allow_empty = RegexValidator(
    regex=r'$|[a-zA-Z]+', message="Data must be entered in Alphabets only.")
alphabet_whitespace_regex = RegexValidator(
    regex=r'[a-zA-Z ]+', message="Data must be entered in Alphabets only.")
alphabet_whitespace_regex_allow_empty = RegexValidator(
    regex=r'$|[a-zA-Z ]+', message="Data must be entered in Alphabets only.")
pincode_regex = RegexValidator(
    regex=r'^[1-9][0-9]{5}$', message="Pincode must be entered in format: '123456'. 6 Characters allowed.")
YEAR_CHOICES = []
for r in range(1950, (datetime.now().year + 1)):
    YEAR_CHOICES.append((r, r))


MALE = 'Male'
FEMALE = 'Female'
OTHER = 'Other'

GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
)


class LifeTimeTrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ActiveObjectManager(models.Manager):

    def get_queryset(self):
        return super(ActiveObjectManager, self).get_queryset().filter(is_active=True)


from django.dispatch import Signal
post_update = Signal()


class UpdateSignalQuerySet(models.query.QuerySet):

    def update(self, kwargs):
        super(MyCustomQuerySet, self).update(kwargs)
        post_update.send(sender=self.model)


class UpdateSignalManager(models.Manager):

    def getqueryset(self):
        return UpdateSignalQuerySet(self.model, using=self._db)


class College(ActiveModel):
    name = models.CharField(blank=False, null=False,
                            max_length=256, unique=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def validate_college(self, college_id):
        is_valid_college = False
        if College.active_objects.get(pk=college_id):
            is_valid_college = True
        return is_valid_college

    class Meta(object):
        db_table = "college"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))


class Company(ActiveModel):
    name = models.CharField(blank=False, null=False,
                            max_length=256, unique=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def validate_company(self, company_id):
        is_valid_company = False
        if Company.active_objects.get(pk=company_id):
            is_valid_company = True
        return is_valid_company

    class Meta(object):
        db_table = "company"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))


class SalaryPaymentMode(ActiveModel):
    name = models.CharField(blank=False, null=False,
                            max_length=256, unique=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "salary_payment_mode"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))


class OrganisationType(ActiveModel):
    name = models.CharField(blank=False, null=False,
                            max_length=256, unique=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "organisation_type"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))
