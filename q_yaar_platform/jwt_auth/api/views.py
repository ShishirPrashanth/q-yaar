import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from common.custom_throttlers import TokenLessAuthAPIThrottleBurst, TokenLessAuthAPIThrottleSustained
from common.decorators import validate_profile
from common.permissions import ActivePermission
from common.response import get_standard_response
from jwt_auth.services.core import (
    svc_auth_check_user_and_profile_exists,
    svc_auth_login,
    svc_auth_refresh_token,
    svc_auth_signup,
    svc_auth_update_password,
    svc_auth_update_profile,
)


class LoginView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".LoginView")
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Login using email and password to get JWT token
        """
        error, response = svc_auth_login(request_data=request.data)
        return get_standard_response(error, response)


class SignupView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".SignupView")
    permission_classes = (AllowAny,)
    throttle_classes = [TokenLessAuthAPIThrottleBurst, TokenLessAuthAPIThrottleSustained]

    def post(self, request, **kwargs):
        """
        Login using email and password to get JWT token
        """
        error, response = svc_auth_signup(request_data=request.data)
        return get_standard_response(error, response)


class TokenRefreshView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".TokenRefreshView")
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        error, response = svc_auth_refresh_token(request_data=request.data)
        return get_standard_response(error, response)


class UserView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".UserView")
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs):
        """
        Check if profile exists for email
        """
        error, response = svc_auth_check_user_and_profile_exists(request_data=request.query_params)
        return get_standard_response(error, response)


class ProfileView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".ProfileView")
    permission_classes = (IsAuthenticated, ActivePermission)

    @validate_profile(logger=logger, allowed_roles=[])
    def patch(self, request, **kwargs):
        error, response = svc_auth_update_profile(
            request_data=request.data, profile=kwargs["profile"], role=kwargs["role"]
        )
        return get_standard_response(error, response)


class PasswordView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".PasswordView")
    permission_classes = (IsAuthenticated, ActivePermission)

    @validate_profile(logger=logger, allowed_roles=[])
    def patch(self, request, **kwargs):
        error, response = svc_auth_update_password(platform_user=request.user, request_data=request.data)
        return get_standard_response(error, response)
