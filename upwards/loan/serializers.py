from django.shortcuts import get_object_or_404
from rest_framework import serializers

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from services.loan_service import BulletLoan

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
        loan_type_object = get_object_or_404(
            models.LoanType, id=self.validated_data.get('loan_type_id', -1))
        cost_breakup_data = 'N.A'
        if loan_type_object.type_name in ['Bullet', 'bullet', 'BULLET']:
            print 1
            bullet_loan = BulletLoan(self.validated_data.get(
                'loan_amount_asked'), self.validated_data.get('loan_type_id'))
            print 2
            cost_breakup_data = bullet_loan.cost_breakup_data()
        data = {
            "heading": "Transfer Details",
            "cost_breakup_data": cost_breakup_data}
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
        loan_type_object = get_object_or_404(
            models.LoanType, id=self.validated_data.get('loan_type_id', -1))
        repayment_schedule_data = 'N.A'
        if loan_type_object.type_name in ['Bullet', 'bullet', 'BULLET']:
            bullet_loan = BulletLoan(self.validated_data.get(
                'loan_amount_asked'), self.validated_data.get('loan_type_id'))
            repayment_schedule_data = bullet_loan.repayment_schedule_data(
                self.validated_data.get('application_date'))
        data = {
            "heading": "Repayment Schedule",
            "repayment_schedule_data": repayment_schedule_data}
        return data
