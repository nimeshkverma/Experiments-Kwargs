from __future__ import unicode_literals

from django.db import models


class LifeTimeTrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Customer(LifeTimeTrackingModel):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    customer_id = models.AutoField(primary_key=True)
    gender = models.CharField(
        max_length=1, default=MALE, choices=GENDER_CHOICES)


class Login(LifeTimeTrackingModel):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'
    PLATFORM_CHOICES = (
        (FACEBOOK, 'Faceebook'),
        (GOOGLE, 'Google Plus'),
    )

    WEB = 'web'
    ANDROID = 'android'
    IOS = 'ios'
    SOURCE_CHOICES = (
        (WEB, 'Web'),
        (ANDROID, 'Android'),
        (IOS, 'IOS'),
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    email_id = models.EmailField()
    platform = models.CharField(
        max_length=20, default=GOOGLE, choices=PLATFORM_CHOICES)
    source = models.CharField(
        max_length=20, default=ANDROID, choices=SOURCE_CHOICES)
    social_data = models.TextField(editable=False, blank=True, null=False)
    platform_token = models.TextField(editable=False, blank=True, null=False)

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer), str(self.email_id), str(self.platform))

    class Meta:
        unique_together = ('email_id', 'platform')
