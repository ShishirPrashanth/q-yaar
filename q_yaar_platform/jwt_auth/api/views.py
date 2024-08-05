import logging

from rest_framework import generics
from rest_framework.permissions import AllowAny

from common.response import get_standard_response
from jwt_auth.services.core import (
    svc_auth_check_user_exists,
    svc_auth_create_new_user,
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
