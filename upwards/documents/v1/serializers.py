from rest_framework import serializers

from documents import models

from common.v1.utils.model_utils import check_pk_existence
from common.v1.exceptions import NotAcceptableError, ConflictError
from customer.models import Customer


class DocumentsSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    document_type_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": Customer, "pk": data.get(
                'customer_id', -1), "pk_name": "customer_id"},
            {"model": models.DocumentType, "pk": data.get(
                'document_type_id', -1), "pk_name": "document_type_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def check_table_conflict(self):
        customer_id = self.validated_data.get('customer_id')
        document_type_id = self.validated_data.get('document_type_id')

        document_objects = models.Documents.objects.filter(
            customer_id=customer_id, document_type_id=document_type_id)
        if document_objects:
            raise ConflictError('customer_id and document_type_id', str(
                customer_id) + ' and ' + str(document_type_id))

    class Meta:
        model = models.Documents
        exclude = ('customer', 'document_type',
                   'created_at', 'updated_at', 'is_active')


class DocumentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DocumentType
        fields = ('id', 'name', 'usage')
