from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from accounts.serializers import UserSerializer
from accounts.models import User


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegistrationSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, min_length=4, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)
    username = serializers.CharField(max_length=128, min_length=4, write_only=True, required=True)
    first_name = serializers.CharField(max_length=50, min_length=2, write_only=True, required=True)
    last_name = serializers.CharField(max_length=50, min_length=2, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','first_name','last_name']

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user