import json
from django.conf import settings
from activity.model_constants import CUSTOMER_STATE_ORDER_LIST, UNKNOWN_STATE
from activity.models import CustomerState
from messenger.models import PreSignupData
from social.models import Login
from pyfcm import FCMNotification


class Notification(object):

    def __init__(self, message_title, message_body, data_message, notification_type):
        self.message_title = message_title if message_title else ''
        self.message_body = message_body if message_body else ''
        self.data_message = self.__jsonify(data_message)
        self.notification_type = notification_type

    def __jsonify(self, data_message):
        try:
            return json.loads(data_message)
        except Exception as e:
            return {}

    def __chunks(self, input_list, chunk_length):
        for i in range(0, len(input_list), chunsk_length):
            yield input_list[i:i + chunk_length]

    def __get_unknown_state_registration_ids(self):
        return PreSignupData.objects.values_list('app_registration_id', flat=True)

    def __get_other_state_registration_ids(self):
        customer_ids = CustomerState.objects.filter(
            present_state=self.notification_type).values_list('app_registration_id', flat=True)
        return Login.objects.filter(customer_ids__in=customer_ids).values_list('app_registration_id', flat=True)

    def __registration_ids(self):
        registration_ids = []
        if self.notification_type == UNKNOWN_STATE:
            registration_ids = self.__get_unknown_state_registration_ids()
        elif self.notification_type in CUSTOMER_STATE_ORDER_LIST:
            registration_ids = self.__get_other_state_registration_ids()
        else:
            pass
        return list(set(registration_ids))

    def send_notifications():
        registration_ids = self.__registration_ids()
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        if not self.data_message:
            for registration_ids_chunk in self.__chunks(registration_ids, 950):
                result = push_service.notify_multiple_devices(
                    registration_ids=registration_ids_chunk, message_title=self.message_title, message_body=self.message_body)
        else:
            for registration_ids_chunk in self.__chunks(registration_ids, 950):
            result = push_service.notify_multiple_devices(
                registration_ids=registration_ids_chunk, data_message=self.data_message, message_body=self.message_body)
