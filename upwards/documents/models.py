from __future__ import unicode_literals

from django.db import models

from common.models import (	ActiveModel,
                            ActiveObjectManager)


UPLOADED = 'uploaded'
VERIFIED = 'verified'

DOCUMENT_STATUS_CHOICES = (
    (UPLOADED, 'uploaded'),
    (VERIFIED, 'verified'),
)


def content_file_name(instance, filename):
    return "{customer_id}/{filename}".format(customer_id=str(instance.customer_id), filename=filename)


class Documents(ActiveModel):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    document_type = models.ForeignKey('DocumentType', on_delete=models.CASCADE)
    document_1 = models.FileField(upload_to=content_file_name)
    document_2 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_3 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_4 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_5 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    document_6 = models.FileField(
        upload_to=content_file_name, blank=True, null=True)
    status = models.CharField(
        max_length=50, default=UPLOADED, choices=DOCUMENT_STATUS_CHOICES)
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    class Meta(object):
        db_table = 'customer_documents'
        unique_together = ('customer', 'document_type')

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.customer), str(self.document_type), str(self.status))


class DocumentType(ActiveModel):
    name = models.CharField(max_length=256, unique=True)
    usage = models.CharField(max_length=256, blank=True, null=True, default='')
    objects = models.Manager()
    active_objects = ActiveObjectManager()

    def __unicode__(self):
        return '%s__%s__%s' % (str(self.id), str(self.name), str(self.usage))

    class Meta(object):
        db_table = 'customer_document_types'
