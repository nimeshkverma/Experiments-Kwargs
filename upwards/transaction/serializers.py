from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import models
from common.utils.model_utils import check_pk_existence
from common.exceptions import NotAcceptableError
from customer.models import Customer
from loan.services.loan_service import BulletLoan
from loan.models import LoanType
from transaction.services.transaction_service import BulletTransaction, TransactionUserState


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

    def loan_request_transactions(self, transaction_status, transaction_type, status_actor):
        loan_type_object = get_object_or_404(
            LoanType, id=self.validated_data.get('loan_type_id', -1))
        data = {
            'loan_id': 'N/A',
            'installment_id': 'N/A',
            'transaction_id': 'N/A',
            'loan_principal': str(self.validated_data.get('loan_amount_asked', 'N/A')),
            'amount_transfered': 'N/A',
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
                transaction_status, transaction_type, status_actor)
            data['loan_id'] = str(loan_object.id)
            data['installment_id'] = str(installment_object.id)
            data['transaction_id'] = str(transaction_object.id)
            data['amount_transfered'] = str(
                bullet_loan.net_amount_credited_field_value())
            bullet_transaction.update_borrower(loan_object.loan_amount_applied)
            TransactionUserState(transaction_status,
                                 transaction_type, status_actor).set_state(self.validated_data.get('customer_id'))
        return data

    def loan_request_transactions_atomic(self, transaction_status, transaction_type, status_actor):
        data = {
            'loan_id': 'N/A',
            'installment_id': 'N/A',
            'transaction_id': 'N/A'
        }
        with transaction.atomic():
            data = self.loan_request_transactions(
                transaction_status, transaction_type, status_actor)
        return data


class TransactionHistorySerializers(serializers.Serializer):
    customer_id = serializers.IntegerField()

    def validate_foreign_keys(self, data=None):
        data = data if data else self.validated_data
        model_pk_list = [
            {'model': Customer, 'pk': data.get(
                'customer_id', -1), 'pk_name': 'customer_id'},
        ]
        for model_pk in model_pk_list:
            if model_pk['pk_name'] in data.keys():
                if not check_pk_existence(model_pk['model'], model_pk['pk']):
                    raise NotAcceptableError(
                        model_pk['pk_name'], model_pk['pk'])

    def transaction_history_data(self):
        transaction_fields = ['loan_id', 'installment_id', 'lender_id',
                              'utr', 'transaction_status', 'transaction_type', 'status_actor']
        transaction_objects = models.Transaction.objects.filter(customer_id=self.validated_data.get(
            'customer_id'), transaction_status=models.COMPLETED).order_by('created_at')
        data_list = []
        for transaction_object in transaction_objects:
            data = {}
            for transaction_field in transaction_fields:
                data[transaction_field] = transaction_object.__dict__.get(
                    transaction_field)
            data_list.append(data)
        return {'customer_id': self.validated_data['customer_id'], 'timeline': data_list}
