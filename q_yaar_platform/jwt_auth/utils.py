################################################
# https://github.com/GetBlimp/django-rest-framework-jwt/tree/master/rest_framework_jwt
################################################

from calendar import timegm
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model

from account.api.serializers import PlatformUserSerializer
from account.models import PlatformUser
from common.jwt import get_base_jwt_payload
from jwt_auth.settings import api_settings


def jwt_get_secret_key_for_user(user: PlatformUser):
    """
    Get unique key for each stored in DB
    """
    return user.auth_secret


def jwt_get_secret_key(payload=None):
    """
    For enhanced security you may want to use a secret key based on user.
    This way you have an option to logout only this user if:
        - token is compromised
        - password is changed
        - etc.
    """
    if api_settings.JWT_GET_USER_SECRET_KEY:
        _user_model = get_user_model()  # noqa: N806
        user = _user_model.objects.get(pk=payload.get("user_id"))
        key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
        return key
    return api_settings.JWT_SECRET_KEY


def jwt_payload_handler(
    user: PlatformUser, profile_role: str = None, profile_suspended: bool = False, expiration_delta=None
):

    payload = get_base_jwt_payload(user, profile_role, profile_suspended)

    if expiration_delta and isinstance(expiration_delta, timedelta):
        token_expiration_time = datetime.utcnow() + expiration_delta
    else:
        token_expiration_time = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA

    payload["exp"] = token_expiration_time

    # Include original issued at time for a brand-new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload["orig_iat"] = timegm(datetime.utcnow().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload["aud"] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload["iss"] = api_settings.JWT_ISSUER

    return payload


def jwt_get_user_id_from_payload_handler(payload):
    """
    Override this function if user_id is formatted differently in payload
    """

    return payload.get("user_id")


def jwt_encode_handler(payload):
    key = api_settings.JWT_PRIVATE_KEY or jwt_get_secret_key(payload)
    return jwt.encode(payload, key, api_settings.JWT_ALGORITHM).decode("utf-8")


def jwt_decode_handler(token):
    #####################################
    # https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py
    # Decode has the following signature
    # def decode(self,
    #           jwt,  # type: str
    #           key='',   # type: str
    #           verify=True,  # type: bool
    #           algorithms=None,  # type: List[str]
    #           options=None,  # type: Dict
    #           **kwargs):
    ########################################
    options = {"verify_exp": api_settings.JWT_VERIFY_EXPIRATION}
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, False)
    secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM],
    )


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    Example:
    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
    """
    return {"token": token, "user": PlatformUserSerializer(user).data}
