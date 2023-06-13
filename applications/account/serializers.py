from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from .models import Renters
from applications.rent.serialisers import RentSerialiser


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True, write_only=True)
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(required = True)
    
    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name',
            'username',
            'email',
            'password',
            'password_confirm',
            'id',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password mismatch')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user  


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    old_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password = serializers.CharField(
        min_length=4, required=True
    )
    new_password_confirm = serializers.CharField(
        min_length=4, required=True
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password_confirm')

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.pop('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Uncorrecct password')
        return old_password

    def set_new_password(self):
        user = self.context['request'].user
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User is not found")
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Password recovery',
            f'Your activation code: {user.activation_code}',
            'example@gmail.com',
            [user.email]
        )


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirm')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('User is not found or wrong activation code')
        if password1 != password2:
            raise serializers.ValidationError('Password mismatch!')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class RentersSerialiser(serializers.ModelSerializer):
    rented_books = RentSerialiser(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Renters


