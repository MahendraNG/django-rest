from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q

import uuid

class RegistrationSerializer(serializers.ModelSerializer):
    """ Signup serializer
        Registration of user and send activation link on user's email
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    def create(self, validated_data):
        record = {}
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.username = validated_data['email']
        user.is_active = False
        user.save()
        user_id = user.id
        access_token = uuid.uuid4()
        token = Token(
                key = str(access_token),
                user_id = user.id
            )
        token.save()
        self.send_email(user_id, validated_data['email'], access_token)
        return user

    def validate(self, data):
        errors = dict()

        if data and len(data['email']) < 1:
            errors['email'] ="Email can not be blank"
        elif User.objects.filter(email=data['email']):
            errors['email'] ="User already exist with this email."

        if errors:
            raise serializers.ValidationError(errors)

        return super(RegistrationSerializer, self).validate(data)
    
    def send_email(self,user_id,email, token):
        subject, from_email = 'Activate your account', 'cis@gmail.com'
        text_content = 'Hi,To confirm your account please check on given links.'
        html_content = "<a href=http://localhost:8000/user_activation_link/"+str(user_id)+"/"+str(token)+"/>Click Here</a>"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'is_active')


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, label="Email", allow_blank = False)
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {"password":{"write_only":True}}
    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]
        if not email and not password:
            raise serializers.ValidationError("Email required for login")
        user = User.objects.filter(Q(email= email)).distinct()
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else :
            raise serializers.ValidationError("This Email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Incorrect Email/Password")
        data["Status"] = "You are logged in now..."
        return data

class UserSerializer(serializers.ModelSerializer):
    """ Userlist serializer
        show userlist
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')