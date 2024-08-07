from django.urls import path

from . import views

app_name = "jwt_auth"

urlpatterns = [
    # POST - Refresh token
    path(r"token/refresh", views.TokenRefreshView.as_view(), name="handler-token"),
    # POST - Verify password and get token
    path(r"token", views.TokenView.as_view(), name="handler-token"),
    # POST - Verify password and get token
    # GET - Check if user exists
    path(r"user", views.UserView.as_view(), name="handler-user"),
    # GET - Get profiles for user
    # POST - Create new profile
    # PATCH - Update profile
    path(r"profiles", views.ProfileView.as_view(), name="handler-profile"),
]
