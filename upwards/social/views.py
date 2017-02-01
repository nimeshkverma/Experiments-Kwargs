from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.decorators import session_authorize, meta_data_response

from . import serializers


class SocialLogin(APIView):

    @meta_data_response()
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            social_login_data = serializer.save()
            return Response(social_login_data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class SocialLogout(APIView):

    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            serializer = serializers.LogoutSerializer(data=auth_data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status.HTTP_204_NO_CONTENT)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


class LinkedinAuth(APIView):

    def authorize_linked(self, request_data):
        serializer = serializer.LinkedinAuthSerializer(request_data)
        if serializer.is_valid():
            serializer.authorize()
            return Response({}, status.HTTP_200_OK)
        return Response({}, status.HTTP_400_BAD_REQUEST)

    @meta_data_response()
    @session_authorize()
    def post(self, request, auth_data):
        if auth_data.get("authorized"):
            return self.authorize_linked(request.data)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @meta_data_response()
    @session_authorize()
    def get(self, request, auth_data):
        if auth_data.get("authorized"):
            return self.authorize_linked(request.GET)
        return Response({}, status.HTTP_401_UNAUTHORIZED)


def linkedin(request):
    if request.method == 'POST':
        print 11010
        authcode = request.body.get('code')
        state = request.body.get('state')
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        header = {'Content-Type': 'application/x-www-form-urlencoded', 'grant_type': 'authorization_code',
                  'code': authcode, 'redirect_uri': "http://8c732110.ngrok.io/customer/linkedin", 'client_id': "81ddg94yp82qla", 'client_secret': "AZT3lJfWhFk0j8W4"}
        print 11010
        r = requests.post(url, data=header)
        r = json.loads(r.text)
        auth_code = r[r.keys()[0]]
        print r, 101
        print authcode
    else:
        print 11010
        authcode = request.GET.get('code')
        state = request.GET.get('state')
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        header = {'Content-Type': 'application/x-www-form-urlencoded', 'grant_type': 'authorization_code',
                  'code': authcode, 'redirect_uri': "http://8c732110.ngrok.io/customer/linkedin", 'client_id': "81ddg94yp82qla", 'client_secret': "AZT3lJfWhFk0j8W4"}
        print 11010
        r = requests.post(url, data=header)
        r = json.loads(r.text)
        auth_code = r[r.keys()[0]]
        print r, 101
        print authcode
    return JsonResponse({
        "meta": {},
        "data": {}
    })
