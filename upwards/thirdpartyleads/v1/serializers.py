from rest_framework import serializers

from thirdpartyleads import models

from common.v1.utils.model_utils import check_pk_existence
from common.v1.exceptions import NotAcceptableError, ConflictError


class ThirdPartyLeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThirdPartyLead
        exclude = ('created_at', 'updated_at', 'is_active')


class ThirdPartyLeadDocumentsSerializer(serializers.ModelSerializer):
    third_party_lead_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {"model": models.ThirdPartyLead, "pk": data.get(
                'third_party_lead_id', -1), "pk_name": "third_party_lead_id"},
        ]
        for model_pk in model_pk_list:
            if model_pk["pk_name"] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def check_table_conflict(self):
        third_party_lead_id = self.validated_data.get('third_party_lead_id')
        document_type = self.validated_data.get('document_type')

        document_objects = models.ThirdPartyLeadDocuments.objects.filter(
            third_party_lead_id=third_party_lead_id, document_type=document_type)
        if document_objects:
            raise ConflictError('third_party_lead_id and document_type', str(
                third_party_lead_id) + ' and ' + str(document_type))

    class Meta:
        model = models.ThirdPartyLeadDocuments
        exclude = ('third_party_lead', 'created_at', 'updated_at', 'is_active')
