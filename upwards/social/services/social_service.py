
import requests
import json

from copy import deepcopy
from django.conf import settings
from social.models import Login

from common.exceptions import ErrorMessage


class SocialProfile(object):
    __email_keys = {
        'google': 'email',
        'facebook': 'email',
        'linkedin': "",
    }

    def __init__(self, platform, platform_token):
        self.__platform = platform
        self.__platform_token = platform_token
        self.__data_urls = {
            "facebook": settings.FACEBOOK['data_url'].format(platform_token=self.__platform_token),
            "google": settings.GOOGLE['data_url'].format(platform_token=self.__platform_token),
            "linkedin": settings.LINKEDIN['data_url'].format(platform_token=self.__platform_token)
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
                'picture', {}).get('data', {}).get(url)
        else:
            self.processed_data['customer_id'] = None
            self.processed_data['email_id'] = None
            self.processed_data['social_data'] = json.dumps(self.data)
            self.processed_data['linkedin_token'] = self.__platform_token
            self.processed_data['linkedin_id'] = self.processed_data.get('id')
            self.processed_data[
                'first_name'] = self.processed_data.get('firstName')
            self.processed_data[
                'last_name'] = self.processed_data.get('lastName')
            self.processed_data['profile_link'] = self.processed_data.get(
                'publicProfileUrl')
            self.processed_data['profile_pic_link'] = self.processed_data.get(
                'pictureUrls', {}).get('values', [None])[0]
            self.processed_data[
                'industry'] = self.processed_data.get('industry')
            self.processed_data['location'] = self.processed_data.get(
                'location', {}).get('name')
            self.processed_data['last_employer'] = self.processed_data.get(
                'values', [{}])[0].get('company', {}).get('name')
            last_job_start_date = self.processed_data.get(
                'values', [{}])[0].get('company', {}).get('startDate', {})
            self.processed_data['join_date_last_employer'] = last_job_start_date.get(
                'year') + '-' + last_job_start_date.get('month') + '-01' if last_job_start_date else None
            self.processed_data['connections'] = self.processed_data[
                'numConnections']


def get_linkedin_token(authcode, state=None):
    auth_url = settings.LINKEDIN['auth_url']
    auth_header = deepcopy(settings.LINKEDIN['auth_header'])
    auth_header['code'] = auth_header['code'].format(authcode=authcode)
    try:
        linkedin_response = request.post(auth_url, auth_header).json()
        linkedin_token = linkedin_response["code"][0]
        return linkedin_token
    except Exception as e:
        return None
