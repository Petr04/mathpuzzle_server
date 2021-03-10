from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password',
            'first_name', 'last_name',
            'token',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    email = serializers.EmailField(read_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('Логин необходим для входа')
        if password is None:
            raise serializers.ValidationError('Пароль необходим для входа')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Неверный логин или пароль')
        if not user.is_active:
            raise serializers.ValidationError('Пользователь отключен')

        return {'token': user.token}

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
