from django.urls import path

from . import views

app_name = "jwt_auth"

urlpatterns = [
    # POST - Login
    path(r"login", views.LoginView.as_view(), name="handler-login"),
    # POST - Sign Up
    path(r"signup", views.SignupView.as_view(), name="handler-signup"),
    # POST - Refresh token
    path(r"token/refresh", views.TokenRefreshView.as_view(), name="handler-token"),
    # GET - Check if user exists
    path(r"user", views.UserView.as_view(), name="handler-user"),
    # PATCH - Update profile
    path(r"profiles", views.ProfileView.as_view(), name="handler-profile"),
    # PATCH - Update password
    path(r"password", views.PasswordView.as_view(), name="handler-password"),
]
