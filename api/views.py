from django.shortcuts import render
from django.contrib.auth.models import User

from oauth2_provider.models import AccessToken
from rest_framework.authtoken.models import Token

from rest_framework import generics
from api.permissions import IsAuthenticatedOrCreate

from api.serializers import RegistrationSerializer
from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope
from django.http import HttpResponse
from  rest_framework.views  import APIView

from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

import json

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