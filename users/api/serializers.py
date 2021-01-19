from typing import Optional

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'phone', 'date_joined',
                  'address', 'is_subscriber', 'subscription_to', 'is_subscriber')
        extra_kwargs = {
            'is_subscriber': {'read_only': True},
            'subscription_to': {'read_only': True},
        }

    def update(self, instance, validated_data) -> User:
        password: Optional[str] = validated_data.pop('password', None)
        user: User = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserRetrieveSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('pk', 'email', 'first_name', 'last_name', 'is_subscriber', 'date_joined')
        extra_kwargs = {
            'is_subscriber': {'read_only': True},
        }


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=5, max_length=255
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'company', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data) -> User:
        password: Optional[str] = validated_data.pop('password')
        instance: User = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
