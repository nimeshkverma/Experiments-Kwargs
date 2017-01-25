import requests
from social.exceptions import ErrorMessage

FACEBOOK_BASE_URL = 'https://graph.facebook.com/me'
GOOGLE_BASE_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

FACEBOOK_KEYS = ['id', 'cover', 'name', 'first_name', 'last_name', 'age_range', 'link', 'gender', 'locale', 'picture', 'timezone', 'updated_time', 'verified',
                 'email']

REQUIRES_FB_REVIEW = ['user_birthday', 'user_education_history', 'user_hometown',
                      'user_location', 'user_managed_groups', 'user_relationships', 'user_work_history']


class SocialProfile(object):
    __google_base_url = GOOGLE_BASE_URL
    __facebook_base_url = FACEBOOK_BASE_URL
    __facebook_keys = FACEBOOK_KEYS
    __email_keys = {
        'google': 'email',
        'facebook': 'email',
    }

    def __init__(self, platform, platform_token):
        self.__platform = platform
        self.__platform_token = platform_token
        self.__data_urls = {
            "facebook": SocialProfile.__facebook_base_url + "?fields=" + ",".join(SocialProfile.__facebook_keys) + "&access_token=" + self.__platform_token,
            "google": SocialProfile.__google_base_url + "?id_token=" + self.__platform_token
        }
        self.data = self.__platform_data()
        self.email_id = self.data.get(
            SocialProfile.__email_keys.get(self.__platform))

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
