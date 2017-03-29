from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from activity.models import register_activity, register_customer_state
from activity.model_constants import (PROFESSIONAL_SUBMIT_STATE, CUSTOMER, PROFESSIONAL_SUBMIT, EDUCATION_SUBMIT_STATE,
                                      EDUCATION_SUBMIT, FINANCE_SUBMIT_EMAIL_VERIFIED_STATE, FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE)
from messenger.models import EmailVerification, PROFESSIONAL
from common.models import (ActiveModel,
                           ActiveObjectManager,
                           YEAR_CHOICES)


# GRADUATE = 'Graduate'
# POST_GRADUATE = 'Post Graduate or Higher'
# OTHERS = 'Others'
# QUALIFICATION_CHOICES = (
#     (GRADUATE, 'graduate'),
#     (POST_GRADUATE, 'post_graduate'),
#     (OTHERS, 'others'),
# )

MARRIED = 'married'
UNMARRIED = 'unmarried'
OTHER_MARITAL_STATUS = 'other'

MARITAL_STATUS_CHOICES = (
    (MARRIED, 'married'),
    (UNMARRIED, 'unmarried'),
    (OTHER_MARITAL_STATUS, 'other'),
)

CAR = 'car'
BIKE = 'bike'
OTHER_VEHICLE_TYPE = 'other'
VEHICLE_TYPE_CHOICES = (
    (CAR, 'car'),
    (BIKE, 'bike'),
    (OTHER_VEHICLE_TYPE, 'other'),
)


class Finance(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    any_active_loans = models.BooleanField(default=False)
    any_owned_vehicles = models.BooleanField(default=False)
    vehicle_type = models.CharField(
        choices=VEHICLE_TYPE_CHOICES, blank=False, null=False, max_length=50, default=OTHER_VEHICLE_TYPE)
    marital_status = models.CharField(
        max_length=50, blank=False, null=False, default=OTHER_MARITAL_STATUS, choices=MARITAL_STATUS_CHOICES)
    dependents = models.IntegerField(null=False, blank=False, default=0)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    @staticmethod
    def register_finance_submit_customer_state(sender, instance, created, **kwargs):
        if created:
            state = FINANCE_SUBMIT_EMAIL_UNVERIFIED_STATE
            profession_object = Profession.objects.get(
                customer_id=instance.customer_id)
            if profession_object.is_email_verified:
                state = FINANCE_SUBMIT_EMAIL_VERIFIED_STATE
            else:
                email_objects = EmailVerification.objects.filter(
                    customer_id=instance.customer_id, email_id=profession_object.email, email_type=PROFESSIONAL)
                if email_objects and email_objects[0].is_verified:
                    state = FINANCE_SUBMIT_EMAIL_VERIFIED_STATE
            register_customer_state(state, instance.customer_id)

    class Meta(object):
        db_table = "customer_finance"

    def __unicode__(self):
        return "%s__any_active_loans:%s__any_owned_vehicles:%s" % (str(self.customer), str(self.any_active_loans), str(self.any_owned_vehicles))


post_save.connect(
    Finance.register_finance_submit_customer_state, sender=Finance)


SELF_EMPLOYED = 'self employed'
SALARIED = 'salaried'
UNEMPLOYED = 'unemployed'
OTHER_NATURE_OF_WORK = 'other'

NATURE_OF_WORK_CHOICES = (
    (SELF_EMPLOYED, 'self employed'),
    (SALARIED, 'salaried'),
    (UNEMPLOYED, 'unemployed'),
    (OTHER_NATURE_OF_WORK, 'other'),
)


class Profession(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    company = models.ForeignKey(
        'common.Company', on_delete=models.CASCADE)
    organisation_type = models.ForeignKey(
        'common.OrganisationType', on_delete=models.CASCADE)
    salary_payment_mode = models.ForeignKey(
        'common.SalaryPaymentMode', on_delete=models.CASCADE)
    profession_type = models.ForeignKey(
        'common.ProfessionType', on_delete=models.CASCADE)
    email = models.EmailField(blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    department = models.CharField(
        max_length=50, blank=True, null=True, default="")
    designation = models.CharField(
        max_length=50, blank=True, null=True, default="")
    office_city = models.CharField(
        max_length=50, blank=True, null=True, default="")
    phone_no = models.CharField(
        max_length=25, blank=True, null=True, default="")
    is_phone_no_verified = models.BooleanField(default=False)
    salary = models.IntegerField(blank=False, null=False)
    join_date = models.DateField(blank=False, null=False)
    total_experience = models.IntegerField(blank=False, null=False, default=0)
    nature_of_work = models.CharField(
        max_length=50, blank=False, null=False, default=OTHER_NATURE_OF_WORK, choices=NATURE_OF_WORK_CHOICES)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def save(self, *args, **kwargs):
        if not self.is_email_verified:
            email_objects = EmailVerification.objects.filter(
                customer_id=self.customer_id, email_id=self.email, email_type=PROFESSIONAL)
            if email_objects:
                self.is_email_verified = email_objects[0].is_verified
        super(Profession, self).save(*args, **kwargs)

    @staticmethod
    def register_proffesional_submit_customer_state(sender, instance, created, **kwargs):
        if created:
            register_customer_state(
                PROFESSIONAL_SUBMIT_STATE, instance.customer_id)

    class Meta(object):
        db_table = "customer_profession"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.company), str(self.salary))

post_save.connect(
    Profession.register_proffesional_submit_customer_state, sender=Profession)


class Education(ActiveModel):
    customer = models.OneToOneField(
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

    @staticmethod
    def register_education_submit_customer_state(sender, instance, created, **kwargs):
        if created:
            register_customer_state(
                EDUCATION_SUBMIT_STATE, instance.customer_id)

    class Meta(object):
        db_table = "customer_education"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.college), str(self.qualification))

post_save.connect(
    Education.register_education_submit_customer_state, sender=Education)


class Vahan(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=50, blank=False, null=False)
    make = models.CharField(max_length=50, blank=True, null=True, default="")
    model = models.CharField(max_length=50, blank=True, null=True, default="")
    make_model = models.CharField(
        max_length=50, blank=True, null=True, default="")
    fuel = models.CharField(max_length=50, blank=True, null=True, default="")
    display_variant = models.CharField(
        max_length=50, blank=True, null=True, default="")
    short_variant = models.CharField(
        max_length=50, blank=True, null=True, default="")
    vehicle_id = models.CharField(
        max_length=50, blank=True, null=True, default="")
    vertical = models.CharField(
        max_length=50, blank=True, null=True, default="")
    rto_code = models.CharField(
        max_length=50, blank=True, null=True, default="")
    rto_lnt_location = models.CharField(
        max_length=50, blank=True, null=True, default="")
    rto_plate_lnt_location = models.CharField(
        max_length=50, blank=True, null=True, default="")
    registration_date = models.CharField(
        max_length=50, blank=True, null=True, default="")
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_vahan"

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.registration_no), str(self.model))
