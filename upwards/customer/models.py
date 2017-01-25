from __future__ import unicode_literals

from django.db import models

from common.models import LifeTimeTrackingModel

MALE = 'M'
FEMALE = 'F'
OTHER = 'O'
GENDER_CHOICES = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
    (OTHER, 'Other'),
)


class Customer(LifeTimeTrackingModel):
    customer_id = models.AutoField(primary_key=True)
    gender = models.CharField(
        max_length=1, default=MALE, choices=GENDER_CHOICES)
