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
        # loan_amount_asked = self.validated_data.get('loan_amount_asked')
        # loan_type_id = self.validated_data.get('loan_type_id')
        # print 100
        # print models.LoanType.objects.get(pk=loan_type_id)
        # return {"q": "q"}
        data = {
            "heading": "Transfer Details",
            "cost_breakup_data": [
                {
                    "field_name": "Loan Principal (Rs)",
                    "field_value": "5000"
                },
                {
                    "field_name": "Processing fee @ 3% (Rs)",
                    "field_value": "-150"
                },
                {
                    "field_name": "Interest fee @ 2% (Rs)",
                    "field_value": "-100"
                },
                {
                    "field_name": "Net amount credited (Rs)",
                    "field_value": "4750"
                }
            ]
        }
        return data


class RepaymentScheduleSerializer(serializers.Serializer):
    loan_amount_asked = serializers.IntegerField()
    loan_type_id = serializers.IntegerField()
    application_date = serializers.DateField()

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

    def repayment_schedule(self):
        data = {
            "heading": "Repayment Schedule",
            "repayment_schedule_data": [
                {
                    "field_name": "Number of Payment Cycles",
                    "field_value": "1"
                },
                {
                    "field_name": "Repayment amount per Cycle (Rs)",
                    "field_value": "5000"
                },
                {
                    "field_name": "Due Date",
                    "field_value": "17 March 2017"
                },
                {
                    "field_name": "Late fee per payment cycle (Rs)",
                    "field_value": "500"
                }
            ]
        }

        return data
