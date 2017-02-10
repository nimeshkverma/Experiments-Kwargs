import requests
import json

from copy import deepcopy
from django.conf import settings

from common.exceptions import ErrorMessage


class SocialProfile(object):
    __email_keys = {
        'google': 'email',
        'facebook': 'email',
    }

    def __init__(self, platform, platform_token):
        self.__platform = platform
        self.__platform_token = platform_token
        self.__data_urls = {
            "facebook": settings.FACEBOOK['data_url'].format(platform_token=self.__platform_token),
            "google": settings.GOOGLE['data_url'].format(platform_token=self.__platform_token),
        }
        self.data = self.__platform_data()
        self.email_id = self.data.get(
            SocialProfile.__email_keys.get(self.__platform))
        self.processed_data = deepcopy(self.data)
        self.__process_data()

    def __fetch_platform_data(self, data_url):
        try:
            data = requests.get(data_url)
            return data.json()
        except Exception as e:
            raise ErrorMessage("Social Media data not found due to: " + str(e))

    def __platform_data(self):
        if self.__data_urls.get(self.__platform):
            return self.__fetch_platform_data(self.__data_urls[self.__platform])
        else:
            raise ErrorMessage("Platform not supported")

    def __process_data(self):
        if self.__platform == 'google':
            self.processed_data['login_id'] = None
            self.processed_data['platform'] = self.__platform
            self.processed_data['platform_id'] = self.processed_data.get('sub')
            self.processed_data[
                'first_name'] = self.processed_data['given_name']
            self.processed_data[
                'last_name'] = self.processed_data['family_name']
            self.processed_data['profile_link'] = "https://plus.google.com/" + \
                str(self.processed_data.get('sub'))
            self.processed_data['gender'] = None
        elif self.__platform == 'facebook':
            self.processed_data['login_id'] = None
            self.processed_data['platform'] = self.__platform
            self.processed_data['platform_id'] = self.processed_data.get('id')
            self.processed_data[
                'profile_link'] = self.processed_data.get('link')
            self.processed_data['profile_pic_link'] = self.processed_data.get(
                'picture', {}).get('data', {}).get('url')
        else:
            raise ErrorMessage("Platform not supported")


class LinkedinProfile(object):

    def __init__(self, code, state=None):
        self.__code = code
        self.__state = state
        self.__auth_token = self.__get_token()
        self.__data_url = settings.LINKEDIN['data_url']
        self.__data_headers = self.__get_data_headers()
        self.data = self.__platform_data()
        self.model_data = self.__get_model_data()

    def __platform_data(self):
        try:
            data = requests.get(self.__data_url, headers=self.__data_headers)
            return data.json()
        except Exception as e:
            raise ErrorMessage("Social Media data not found due to: " + str(e))

    def __get_data_headers(self):
        headers = settings.LINKEDIN['data_auth']
        headers['Authorization'] = headers['Authorization'].format(
            platform_token=self.__auth_token)
        return headers

    def __get_token(self):
        auth_url = settings.LINKEDIN['auth_url']
        auth_header = deepcopy(settings.LINKEDIN['auth_header'])
        auth_header['code']
        auth_header['code'] = auth_header[
            'code'].format(code=self.__code)
        try:
            linkedin_response = requests.post(auth_url, auth_header).json()
            linkedin_token = linkedin_response["code"][0]
            return linkedin_token
        except Exception as e:
            return None

    def __get_model_data(self):
        last_job_start_date = self.data.get('values', [{}])[0].get(
            'company', {}).get('startDate', {})
        model_data = {
            'auth_token': self.__auth_token,
            'social_data': json.dumps(self.data),
            'email_id': self.data.get('email_id'),
            'linkedin_id': self.data.get('id'),
            'first_name': self.data.get('firstName'),
            'last_name': self.data.get('lastName'),
            'gender': self.data.get('gender'),
            'profile_link': self.data.get('publicProfileUrl'),
            'profile_pic_link': self.data.get('pictureUrls', {}).get('values', [None])[0],
            'industry': self.data.get('industry'),
            'location': self.data.get('location', {}).get('name'),
            'last_employer': self.data.get('values', [{}])[0].get('company', {}).get('name'),
            'join_date_last_employer': last_job_start_date.get('year') + '-' + last_job_start_date.get('month') + '-01' if last_job_start_date else None,
            'connections': self.data.get('numConnections', 0)

        }
        return model_data
