from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
import uuid

class RegistrationSerializer(serializers.ModelSerializer):
    """ Signup serializer
        Registration of user and send activation link on user's email
    """
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username= validated_data['first_name'] + " " + validated_data['last_name']            
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()

        access_token = uuid.uuid4()
        token = Token(
                key = str(access_token),
                user_id = user.id
            )
        token.save()
        self.send_email(validated_data['email'], access_token)        
        return user

    def validate(self, data):
        errors = dict()
        if data and len(data['email']) < 1:
            errors['email'] ="Email can not be blank"
        if errors:
            raise serializers.ValidationError(errors)
        return super(RegistrationSerializer, self).validate(data)

    def send_email(self, email, token):
        subject, from_email = 'Activate your account', 'cis@gmail.com'
        text_content = 'Hi,To confirm your account please check on given links.'
        html_content = '<a href="#"">Click Here</a>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'is_active')