################################################################################################
# https://github.com/GetBlimp/django-rest-framework-jwt/tree/master/rest_framework_jwt
################################################################################################
import jwt

from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from account.models import PlatformUser
from jwt_auth.settings import api_settings
from datetime import datetime, timedelta
from calendar import timegm

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_user_id_from_payload_handler = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_str(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = "Invalid Authorization header. No credentials provided."
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Invalid Authorization header. Credentials string should not contain spaces."
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication. Otherwise, returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = "Signature has expired."
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = "Error decoding signature."
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        except PlatformUser.DoesNotExist:
            msg = "Platform User doesn't exist"
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)

        return user, payload

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        _user_model = get_user_model()
        user_id = jwt_get_user_id_from_payload_handler(payload)

        if not user_id:
            msg = "Invalid payload."
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = _user_model.objects.get(pk=user_id)
        except _user_model.DoesNotExist:
            msg = "Invalid signature."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User account is disabled."
            raise exceptions.AuthenticationFailed(msg)

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `JWT_AUTH_HEADER_PREFIX`. For example:
        Authorization: JWT eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """

    www_authenticate_realm = "api"

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)


class RefreshJSONWebToken(BaseJSONWebTokenAuthentication):
    """
    Returns a refreshed access token (with new expiration) based on existing access token

    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """

    def validate_and_refresh_token(self, token: str, user: PlatformUser):
        try:
            unverified_payload = jwt.decode(token, None, False)
        except jwt.DecodeError:
            raise ValueError("Invalid jwt token - not able to decode")

        # ensuring token belongs to user
        # payload(that we get from token) contains phone number of user , checking if user's phone and payload's phone are same
        if user.email != unverified_payload.get("email"):
            raise ValueError("Token does not belong to user.")

        # Get and check 'orig_iat'
        orig_iat = unverified_payload.get("orig_iat")
        now_timestamp = timegm(datetime.utcnow().utctimetuple())
        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = refresh_limit.days * 24 * 3600 + refresh_limit.seconds

            expiration_timestamp = orig_iat + int(refresh_limit)

            if now_timestamp > expiration_timestamp:
                msg = "Refresh has expired."
                raise exceptions.AuthenticationFailed(msg)
        else:
            msg = "orig_iat field is required."
            raise exceptions.AuthenticationFailed(msg)

        new_payload = jwt_payload_handler(user)
        new_payload["orig_iat"] = now_timestamp

        return jwt_encode_handler(new_payload), user
