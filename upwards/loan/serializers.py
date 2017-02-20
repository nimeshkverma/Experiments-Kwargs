from rest_framework import serializers

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError

from . import models


class LoanTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.LoanType
        exclude = ('created_at', 'updated_at')


class CostBreakupSerializer(serializers.Serializer):
    loan_amount_asked = serializers.IntegerField()
    loan_type_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {'model': models.LoanType, 'pk': data.get(
                'loan_type_id', -1), 'pk_name': 'id'},
        ]
        for model_pk in model_pk_list:
            if model_pk['pk_name'] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def cost_breakup(self):
        loan_amount_asked = self.validated_data.get('loan_amount_asked')
        loan_type_id = self.validated_data.get('loan_type_id')
        print 100
        print models.LoanType.objects.get(pk=loan_type_id)
        return {"q": "q"}
