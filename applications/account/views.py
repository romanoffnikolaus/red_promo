from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import User, Renters


User = get_user_model()


class PermissionMixin:
    permission_classes = [IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    @swagger_auto_schema(request_body=serializers.RegistrationSerializer, tags=['Account'])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(PermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            message = 'Successful'
            return Response(serializer.validated_data)
        else:
            message = 'Uncorrecct password'
            return Response(message)
        

class ForgotPasswordView(PermissionMixin, APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('You will receive a link to reset your password.')


class ForgotPasswordCompleteView(PermissionMixin, APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordCompleteSerializer, tags=['Account'])
    def post(self, request):
        serializer = serializers.ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(serializer.validated_data)


class LoginView(TokenObtainPairView):

    @swagger_auto_schema(tags=['Account'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except Exception:
            return  Response({'error':'Invalid email'}, status=401)
        user_data = {'id': user.id}
        new_data = list(user_data.items())
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data.update(new_data)
        return Response(serializer.validated_data, status=200)
    

class RentersView(ModelViewSet):
    queryset = Renters.objects.all()
    serializer_class = serializers.RentersSerialiser