from django.shortcuts import get_object_or_404
from rest_framework import serializers

from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from loan.services.loan_service import BulletLoan
from transaction.services.transaction_service import BulletTransaction

from . import models
from customer.models import Customer
from loan.models import LoanType


class LoanRequestTransactionSerializers(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount_asked = serializers.IntegerField()
    loan_type_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {'model': LoanType, 'pk': data.get(
                'loan_type_id', -1), 'pk_name': 'id'},
            {'model': Customer, 'pk': data.get(
                'customer_id', -1), 'pk_name': 'customer_id'},
        ]
        for model_pk in model_pk_list:
            if model_pk['pk_name'] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def loan_request_transactions(self):
        loan_type_object = get_object_or_404(
            LoanType, id=self.validated_data.get('loan_type_id', -1))
        data = {
            'loan_id': 'N/A',
            'installment_id': 'N/A',
            'transaction_id': 'N/A'
        }
        if loan_type_object.type_name in ['Bullet', 'bullet', 'BULLET']:
            bullet_loan = BulletLoan(self.validated_data.get(
                'loan_amount_asked'), self.validated_data.get('loan_type_id'))
            loan_object = bullet_loan.create_loan(self.validated_data.get(
                'customer_id'))
            installment_object = bullet_loan.create_installments()
            bullet_transaction = BulletTransaction(
                loan_object.customer_id, loan_object.id, loan_object.lender_id, installment_object.id)
            transaction_object = bullet_transaction.create_loan_request_transaction(
                models.INITIATED, models.LOAN_AVAIL, models.UPWARDS)
            data['loan_id'] = str(loan_object.id)
            data['installment_id'] = str(installment_object.id)
            data['transaction_id'] = transaction_object.id
        return data
