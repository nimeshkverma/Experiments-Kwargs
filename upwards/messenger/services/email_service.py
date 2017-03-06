from django.core import signing
from django.core.mail import EmailMultiAlternatives
from rest_framework.reverse import reverse
from django.template.loader import get_template

from django.conf import settings
from customer.models import Customer
from eligibility.models import Profession
from activity.models import register_activity, register_customer_state
from activity.model_constants import FINANCE_SUBMIT_EMAIL_VERIFIED_STATE, DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE


def send_verification_mail(email_verify_data):
    encoded_data = signing.dumps(email_verify_data)
    verification_link = settings.BASE_URL + 'customer/verify_email/' + encoded_data
    template = get_template('messenger/email_verify.html')
    html_part = template.render({'verification_link': verification_link})
    msg = EmailMultiAlternatives('Email verification Link, Upwards',
                                 None, 'upwardstech@gmail.com', [email_verify_data['email_id']])
    msg.attach_alternative(html_part, 'text/html')
    msg.send(True)


email_model_fields = {
    'customer_alternate_email': {
        'model': Customer,
        'email_verified_field': 'is_alternate_email_id_verified',
        'user_state': DOCUMENT_SUBMIT_EMAIL_VERIFIED_STATE,
    },
    'customer_profession_email': {
        'model': Profession,
        'email_verified_field': 'is_email_verified',
        'user_state': FINANCE_SUBMIT_EMAIL_VERIFIED_STATE,
    }
}


def update_email_models(email_object):
    if email_object.email_type in email_model_fields.keys():
        email_model = email_model_fields[email_object.email_type]['model']
        email_verified_field = email_model_fields[
            email_object.email_type]['email_verified_field']
        email_model.objects.filter(customer_id=email_object.customer.customer_id).update(
            **{email_verified_field: email_object.is_verified})
        register_customer_state(email_model_fields[email_object.email_type][
            'user_state'], email_object.customer_id)
