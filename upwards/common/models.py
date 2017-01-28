from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models

mobile_number_regex = RegexValidator(
    regex=r'^$|\d{10}$', message="Mobile number must be entered in the format: '9999999999'. 10 digits allowed.")

MALE = 'M'
FEMALE = 'F'
OTHER = 'O'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
)
# gender = models.CharField(max_length=1, default=MALE, choices=GENDER_CHOICES)


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


class College(ActiveModel):
    name = models.CharField(blank=False, null=False, max_length=256)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "college"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))


class Company(ActiveModel):
    name = models.CharField(blank=False, null=False, max_length=256)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "company"

    def __unicode__(self):
        return "%s__%s" % (str(self.id), str(self.name))
