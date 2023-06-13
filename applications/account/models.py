from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()


class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)    
    activation_code = models.CharField(max_length=10, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def create_activation_code(self):
        code = get_random_string(10)
        self.activation_code = code
        self.save()
    
    class Meta:
        indexes = [models.Index(fields=['email']),]


class Renters(models.Model):
    name = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    adress = models.CharField(max_length=50, blank=True)
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        indexes = [models.Index(fields=['email']),]