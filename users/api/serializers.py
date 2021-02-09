from typing import Optional

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'client_id', 'phone', 'date_joined',
                  'address', 'is_subscriber', 'image', 'monthly_views', 'has_access')
        extra_kwargs = {
            'client_id': {'read_only': True},
            'is_subscriber': {'read_only': True},
            'monthly_views': {'read_only': True},
            'has_access': {'read_only': True}
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
        fields = ('pk', 'email', 'first_name', 'last_name', 'is_subscriber', 'date_joined', 'image', 'client_id')
        extra_kwargs = {
            'client_id': {'read_only': True},
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
        fields = ('email', 'first_name', 'last_name', 'password', 'client_id')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'client_id': {'read_only': True}
        }

    def create(self, validated_data) -> User:
        password: Optional[str] = validated_data.pop('password')
        instance: User = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
