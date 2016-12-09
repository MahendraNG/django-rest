from django.shortcuts import render
from django.contrib.auth.models import User

from oauth2_provider.models import AccessToken
from rest_framework.authtoken.models import Token

from rest_framework import generics
from api.permissions import IsAuthenticatedOrCreate

from api.serializers import RegistrationSerializer, UserLoginSerializer

from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope
from django.http import HttpResponse
from  rest_framework.views  import APIView

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import json
import os
import subprocess

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAuthenticatedOrCreate,)


class UserActivation(generics.UpdateAPIView):   
    def get(self, request, token, user_id,format=None):
        user_obj = User.objects.get(id = user_id)
        token_obj = Token.objects.get(user_id = user_obj)
        if user_obj.is_active == 0:
            if token_obj:
                key = token_obj.key
                if key == token:
                    user_obj.is_active = 1
                    user_obj.save(update_fields=['is_active'])
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'your registration has been activated'
            return HttpResponse(json.dumps(serialized_user), content_type = "application/json")
        else:
            serializer = RegistrationSerializer(user_obj)
            serialized_user = serializer.data
            serialized_user['message'] = 'Activation already Done'
            return HttpResponse(json.dumps(serialized_user), content_type = "application/json")

class UserAPILoginView (APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    def post(self, request, * args, ** kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            cmd = 'curl -X POST -d "grant_type=password&username=cis&password=admin123" -u "clientiddddd:clientsecresttttt" localhost:8000/o/token/'
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            resp = subprocess.check_output(['bash','-c', cmd])
            resp = json.loads(resp)
            new_data['access_token'] = resp['access_token']
            new_data['token_type'] = resp['token_type']
            new_data['expires_in'] = resp['expires_in']
            new_data['refresh_token'] = resp['refresh_token']
            new_data['scope'] = resp['scope']
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)