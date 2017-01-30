from __future__ import unicode_literals

from django.db import models

from common.models import (ActiveModel,
                           ActiveObjectManager,
                           YEAR_CHOICES)


GRADUATE = 'Graduate'
POST_GRADUATE = 'Post Graduate or Higher'
OTHERS = 'Others'
QUALIFICATION_CHOICES = (
    (GRADUATE, 'graduate'),
    (POST_GRADUATE, 'post_graduate'),
    (OTHERS, 'others'),
)


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


class Profession(ActiveModel):
    customer = models.ForeignKey(
        'customer.Customer', on_delete=models.CASCADE)
    company = models.ForeignKey(
        'common.Company', on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    phone_no = models.CharField(
        max_length=25, blank=True, null=True, default="")
    is_phone_no_verified = models.BooleanField(default=False)
    salary = models.IntegerField(blank=False, null=False)
    join_date = models.DateField(blank=False, null=False)
    total_experience = models.DecimalField(
        blank=False, null=False, default=0.0, decimal_places=2, max_digits=4)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_profession"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.company), str(self.salary))


class Education(ActiveModel):
    customer = models.ForeignKey(
        'customer.Customer', on_delete=models.CASCADE)
    college = models.ForeignKey(
        'common.College', on_delete=models.CASCADE)
    qualification = models.CharField(max_length=25, blank=False, null=False)
    completion_year = models.IntegerField(
        choices=YEAR_CHOICES, blank=False, null=False)
    qualification_type = models.CharField(
        max_length=25, blank=False, null=False, default="highest")
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_education"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.college), str(self.qualification))
