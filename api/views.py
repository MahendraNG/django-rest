
from django.contrib.auth.models import User
from oauth2_provider.models import AccessToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from api.permissions import IsAuthenticatedOrCreate
from api.serializers import (
    RegistrationSerializer, UserLoginSerializer, UserSerializer,
    ChangePasswordSerializer)
from oauth2_provider.ext.rest_framework import TokenHasScope
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.conf import settings

import json
import subprocess


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Registeration successfully, please check your email for activate account.', 'data': serializer.data , 'error': "0"})
        else:
            try:
                return Response({'message': serializer.errors['message'], 'data': serializer.errors['data'], 'error': serializer.errors['error'][0]})
            except KeyError:
                return Response({'message': [x[0] for x in tuple(serializer.errors.values()) ][0], 'data': serializer.data, 'error': "1"})


class UserActivation(generics.UpdateAPIView):

    def get(self, request, token, user_id, format=None):
        user_obj = User.objects.get(id=user_id)
        token_obj = Token.objects.get(user_id=user_obj)
        if user_obj.is_active == 0:
            if token_obj:
                key = token_obj.key
                if key == token:
                    user_obj.is_active = 1
                    user_obj.save(update_fields=['is_active'])
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'your registration has been activated'
            return HttpResponse({'data': serialized_user, 'message': 'your registration has been activated', 'error': "0"})
        else:
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'Activation already Done'
            serialized_user['error'] = "0"
            serialized_user['data'] = ''
            return HttpResponse(json.dumps(serialized_user), content_type="application/json")


class UserAPILoginView (APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, * args, ** kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():

            new_data = serializer.data
            cmd = 'curl -X POST -d "grant_type=password&username=%s&password=%s" -u "%s:%s" http://beta.cisin.com:3008/o/token/' % (
                data['email'], data['password'], settings.CLIENT_ID, settings.CLIENT_SECRET)
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            resp = subprocess.check_output(['bash', '-c', cmd])
            resp = json.loads(resp.decode('utf-8'))
            new_data['access_token'] = resp['access_token']
            new_data['token_type'] = resp['token_type']
            new_data['expires_in'] = resp['expires_in']
            new_data['refresh_token'] = resp['refresh_token']
            new_data['scope'] = resp['scope']

            return Response({'data':new_data, 'message': 'Login Successful', 'error': "0"})

        return Response({'message': serializer.errors['message'][0], 'data': serializer.errors['data'], 'error': serializer.errors['error'][0]})
        # return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    required_scopes = ['read']
    serializer_class = UserSerializer
    permission_classes = [TokenHasScope]

    def get(self, request, *args, **kwargs):

        serializer = self.get_serializer()

        data = []
        for user in User.objects.all():
            data.append({'id': user.id, 'email': user.email, 'firstname': user.first_name, 'lasename': user.last_name})
        return Response({'error': "0", 'message': "user lists", 'data':data })


        if serializer.is_valid():
            return Response({'message': 'Registeration successfully, please check your email for activate account.', 'data': serializer.data , error: "0"})
        else:
            try:
                return Response({'message': serializer.errors['message'], 'data': serializer.errors['data'], 'error': serializer.errors['error'][0]})
            except Exception as e:
                return Response({'message': serializer.errors['password'], 'data': serializer.data, 'error': "1"})


class ChangePassword(generics.UpdateAPIView):
    """ Change password API """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            newpassword = request.data['newpassword']
            access_token = request.data['token']
            confirm_password = request.data['confirm_password']

            if newpassword != confirm_password:
                return Response({"message": "Password not matches.", "error": "1", 'data': serializer.data})

            try:
                token = AccessToken.objects.get(token=access_token)
            except AccessToken.DoesNotExist:
                return Response({"message": "Access token not matches.", 'error': "1", 'data': serializer.data})

            user_id = token.user_id
            user_detail = User.objects.get(id=user_id)

            if not user_detail.check_password(serializer.data.get("old_password")):
                return Response({"message": "Wrong password.", 'error': "1", 'data': serializer.data})

            # set_password also hashes the password that the user will get
            user_detail.set_password(serializer.data.get("newpassword"))
            user_detail.save()
            return Response({"message": 'Password has been changed successfully.', 'error': "0", 'data': serializer.data})
        else:
            return Response({"message": 'There is some fileds are missing, please try again!', 'error': "1", 'data': serializer.data})
