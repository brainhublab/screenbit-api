from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

from django.core.cache import cache

from .models import User, get_serialized_user_cache_key


class CustomRegisterSerializer(RegisterSerializer):
    """
    User serializer on registration process
    """
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    organization = serializers.CharField(max_length=60, allow_blank=True)

    bio = serializers.CharField(
        max_length=500, required=False, allow_blank=True)
    phone = serializers.CharField(
        max_length=100, required=False, allow_blank=True)

    country_id = serializers.CharField(
        max_length=100, required=True, allow_blank=False)
    country = serializers.CharField(
        max_length=100, required=True, allow_blank=False)
    address = serializers.CharField(
        max_length=100, required=True, allow_blank=False)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            organization=validated_data['organization'],
            phone=validated_data['phone'],
            bio=validated_data['bio'],
            country_id=validated_data['country_id'],
            country=validated_data['country'],
            address=validated_data['address']
        )
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    wat
    """
    class Meta:
        model = User
        fields = ('email')
        read_only_fields = ('email',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Main user serializer
    """

    class Meta:
        model = User
        fields = ('id', 'url', 'bio', 'first_name', 'last_name',
                  'image', 'date_joined', 'last_active', 'is_online')
        read_only_fields = fields


class PrivateUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    User serializer with private info
    """

    class Meta:
        model = User
        fields = ('id', 'url', 'email', 'phone', 'bio', 'first_name', 'last_name', 'image',
                  'is_online', 'is_verified_email')

        read_only_fields = ('id', 'url', 'is_online', 'last_active', 'is_verified_email')
