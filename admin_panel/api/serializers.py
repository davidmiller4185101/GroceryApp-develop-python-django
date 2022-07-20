import datetime
from django.utils import timezone
from rest_framework import serializers
from admin_panel.models import Category, Highlights, CustomUser
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as api_reverse

jwt_payload_handler             = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler              = api_settings.JWT_ENCODE_HANDLER
expire_delta                    = api_settings.JWT_REFRESH_EXPIRATION_DELTA

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'img']


class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlights
        fields = ['title', 'img']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'url', 'email', 'phone_number', 'last_name', 'first_name', 'is_staff', 'user_type']


class UserRegisterSerializer(serializers.ModelSerializer):
    password2           = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token               = serializers.SerializerMethodField(read_only=True)
    expires             = serializers.SerializerMethodField(read_only=True)
    message             = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'phone_number',
            'email',
            'password',
            'password2',
            'token',
            'expires',
            'message',
        ]

        extra_kwargs = {'password': {'write_only': True}}

    def get_message(self, obj):
        return "Thank you for registering."

    def get_expires(self, obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def validate_email(self, value):
        qs = CustomUser.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate_phone_number(self, value):
        qs = CustomUser.objects.filter(phone_number__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this phone number already exists")
        return value

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):  
        user_obj = CustomUser(phone_number=validated_data.get('phone_number'), email=validated_data.get('email'))
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj