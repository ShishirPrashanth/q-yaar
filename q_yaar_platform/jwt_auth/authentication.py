from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from account.models import PlatformUser


class JWTAccessToken(AccessToken):
    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)
        self["role"] = role

    @classmethod
    def for_user(cls, user: PlatformUser, role: str = None):
        token = super().for_user(user)
        # Add custom claims based on user object
        token["email"] = user.email
        token["phone"] = user.phone
        token["is_active"] = user.is_active
        token["is_suspended"] = user.is_suspended
        token["role"] = role
        return token


class JWTRefreshToken(RefreshToken):
    def __init__(self, *args, **kwargs):
        role = kwargs.pop("role", None)
        super().__init__(*args, **kwargs)
        self["role"] = role

    @classmethod
    def for_user(cls, user: PlatformUser, role: str = None):
        token = super().for_user(user)
        # Add custom claims based on user object
        token["email"] = user.email
        token["phone"] = user.phone
        token["is_active"] = user.is_active
        token["is_suspended"] = user.is_suspended
        token["role"] = role
        return token
