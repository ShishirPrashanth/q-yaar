from django.urls import path

from . import views

app_name = "jwt_auth"

urlpatterns = [
    # POST - Verify password and get token
    path(r"token", views.TokenView.as_view(), name="handler-token"),
    # POST - Verify password and get token
    # GET - Check if user exists
    path(r"user", views.UserView.as_view(), name="handler-user"),
]
