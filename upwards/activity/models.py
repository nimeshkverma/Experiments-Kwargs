from __future__ import unicode_literals

from django.db import models

from common.models import ActiveModel, ActiveObjectManager
from model_constants import (CUSTOMER_STATE_CHOICES, ACTOR_CHOICES, CUSTOMER, ACTIVITY_TYPE_CHOICES,
                             SIGN_UP, SIGN_UP_STATE, UNKNOWN_STATE, CUSTOMER_STATE_ORDER_LIST, CUSTOMER_STATE_TREE)


class CustomerState(ActiveModel):
    customer = models.OneToOneField(
        'customer.Customer', on_delete=models.CASCADE)
    present_state = models.CharField(
        max_length=100, default=SIGN_UP_STATE, choices=CUSTOMER_STATE_CHOICES)
    from_state = models.CharField(
        max_length=100, default=UNKNOWN_STATE, choices=CUSTOMER_STATE_CHOICES)
    to_state = models.CharField(
        max_length=100, default=None, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    @staticmethod
    def get_customer_present_state(customer_id):
        customer_state_object = CustomerState.objects.get(
            customer_id=customer_id)
        return customer_state_object.present_state

    class Meta(object):
        db_table = "customer_state"

    def __unicode__(self):
        return "%s__%s-->%s-->%s" % (str(self.customer_id), str(self.from_state), str(self.present_state), str(self.to_state))


class Activity(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    actor = models.CharField(
        max_length=100, default=CUSTOMER, choices=ACTOR_CHOICES)
    activity_type = models.CharField(
        max_length=100, default=SIGN_UP, choices=ACTIVITY_TYPE_CHOICES)
    comments = models.TextField(blank=True, null=True)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = "customer_activity"
        unique_together = ('customer', 'actor', 'activity_type')

    def __unicode__(self):
        return "%s__%s__%s" % (str(self.customer_id), str(self.actor), str(self.activity_type))


def register_activity(activity_type, actor, customer_id, comments=None):
    activity_objects = Activity.objects.filter(
        customer_id=customer_id, actor=actor, activity_type=activity_type)
    if not activity_objects:
        Activity.objects.create(customer_id=customer_id,
                                actor=actor, activity_type=activity_type, comments=comments)
    for activity_object in activity_objects:
        activity_object.update()


def register_customer_state(present_state, customer_id, comments=None):
    state_objects = CustomerState.objects.filter(
        customer_id=customer_id)
    if state_objects:
        state_object = state_objects[0]
        from_state = state_object.present_state
        if (present_state in CUSTOMER_STATE_TREE.get(from_state, {}).get('to')) and (from_state in CUSTOMER_STATE_TREE.get(present_state, {}).get('from')):
            state_object.from_state = from_state
            state_object.present_state = present_state
            state_object.save()
    else:
        if present_state == SIGN_UP_STATE:
            CustomerState.objects.create(customer_id=customer_id)
