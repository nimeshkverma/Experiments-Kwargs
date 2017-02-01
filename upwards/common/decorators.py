from functools import wraps
from django.db import IntegrityError
from rest_framework import status
from serializers import AuthenticationSerializer
from response import MetaDataResponse
from exceptions import NotAcceptableError


def session_authorize(customer_id_key='pk', *args, **kwargs):
    def deco(f):
        def abstract_customer_id(request):
            if request.method == 'GET':
                customer_id = request.query_params.get(customer_id_key)[0]
            else:
                customer_id = request.data.get(customer_id_key)
            return customer_id

        def abstract_session_token(request):
            session_token_header_key = 'HTTP_SESSION_TOKEN'
            return request.META.get(session_token_header_key)

        @wraps(f)
        def decorated_function(*args, **kwargs):
            request = args[1]
            if kwargs.get(customer_id_key):
                customer_id = kwargs[customer_id_key]
                kwargs.pop(customer_id_key)
            else:
                customer_id = abstract_customer_id(request)
            auth_data = {
                'customer_id': customer_id,
                'session_token': abstract_session_token(request)
            }
            auth_serializer = AuthenticationSerializer(data=auth_data)
            auth_data['authorized'] = auth_serializer.is_valid(
            ) and auth_serializer.verify_and_update_session()
            return f(auth_data=auth_data, *args, **kwargs)
        return decorated_function
    return deco


def catch_exception(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except NotAcceptableError as e:
            return MetaDataResponse(e.response, e.meta, status=e.status)
        except IntegrityError as e:
            return MetaDataResponse({}, str(e), status=status.HTTP_409_CONFLICT)
    return decorated_function


def meta_data_response(meta=""):
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            vanilla_response = f(*args, **kwargs)
            return MetaDataResponse(vanilla_response.data, meta, status=vanilla_response.status_code)
        return decorated_function
    return deco
