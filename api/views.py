from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics
from api.permissions import IsAuthenticatedOrCreate
from api.serializers import RegistrationSerializer

import json

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAuthenticatedOrCreate,)
