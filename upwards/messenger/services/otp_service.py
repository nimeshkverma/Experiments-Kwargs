import requests
from django.conf import settings


def send_otp(otp_data):
    message = str(otp_data['otp_code']) + settings.POST_OTP_MESSAGE
    data = {
        'apiKey': settings.SMS_GATEWAY_API_KEY,
        'numbers': otp_data['mobile_number'],
        'message': message, 'sender': settings.SMS_SENDER_NAME
    }
    response = requests.post(settings.SMS_GATEWAY_URL, data=data)
