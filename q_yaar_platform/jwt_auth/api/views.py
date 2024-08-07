import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from common.decorators import validate_profile
from common.permissions import ActivePermission
from common.response import get_standard_response
from jwt_auth.services.core import (
    svc_auth_check_user_exists,
    svc_auth_create_new_user,
    svc_auth_create_profile_for_user,
    svc_auth_get_all_profiles_for_user,
    svc_auth_refresh_token,
    svc_auth_verify_password_and_get_token,
)


class TokenView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".TokenView")
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Verify password and get JWT token
        """
        error, response = svc_auth_verify_password_and_get_token(request_data=request.data)
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

    def post(self, request, **kwargs):
        """
        Signup for new user
        """
        error, response = svc_auth_create_new_user(request_data=request.data)
        return get_standard_response(error, response)

    def get(self, request, **kwargs):
        """
        Check if profile exists for email
        """
        error, response = svc_auth_check_user_exists(request_data=request.query_params)
        return get_standard_response(error, response)


class ProfileView(generics.GenericAPIView):
    logger = logging.getLogger(__name__ + ".ProfileView")
    permission_classes = (IsAuthenticated, ActivePermission)
    authentication_classes = (JWTAuthentication,)

    @validate_profile(logger=logger, allowed_roles=[])
    def get(self, request, **kwargs):
        error, response = svc_auth_get_all_profiles_for_user(platform_user=request.user)
        return get_standard_response(error, response)

    def post(self, request, **kwargs):
        error, response = svc_auth_create_profile_for_user(request_data=request.data, platform_user=request.user)
        return get_standard_response(error, response)
