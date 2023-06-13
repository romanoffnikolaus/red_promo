from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)

from . import views


router = DefaultRouter()
router.register('genres', views.RentersView)

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="user_registration"),
    path('change-password/', views.ChangePasswordView.as_view(), name="change_password"),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name="forgot_password"),
    path('forgot_password_complete/',views.ForgotPasswordCompleteView.as_view()),
    path('login/', views.LoginView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh")
]
