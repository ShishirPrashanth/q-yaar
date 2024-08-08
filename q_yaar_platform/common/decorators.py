import jwt

from django.conf import settings

from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from account.cache import set_lastlogin_for_user_id
from common.constants import UserRolesType
from jwt_auth.services.interfacer import svc_auth_get_profile_for_user_and_role


def validate_profile(logger, allowed_roles: list[UserRolesType] = []):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[1]

            try:
                decoded_token = jwt.decode(str(request.auth), settings.SECRET_KEY, algorithms=["HS256"])
            except jwt.DecodeError:
                return Response({"detail": "Error decoding signature"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return Response({"detail": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"detail": "Invalid token passed"}, status=status.HTTP_401_UNAUTHORIZED)

            user = request.user
            role = (
                UserRolesType.tokentype_from_string(decoded_token.get("role")) if decoded_token.get("role") else None
            )

            error, profile = svc_auth_get_profile_for_user_and_role(platform_user=user, role=role)
            if error:
                return Response(
                    {
                        "detail": f"{decoded_token.get('role')} profile does not exist for user - {str(profile.get_external_id())}"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            if profile:
                if profile.is_suspended:
                    return Response({"detail": "Profile has been suspended"}, status=status.HTTP_403_FORBIDDEN)

                if profile.is_deleted or profile.platform_user.is_deleted:
                    return Response({"detail": "Account has been deleted"}, status=status.HTTP_401_UNAUTHORIZED)

                if allowed_roles and role not in allowed_roles:
                    return Response(
                        {
                            "detail": f"Invalid role. Only allowed for {','.join([role.name if role else 'GUEST' for role in allowed_roles])}"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            kwargs["role"] = role
            kwargs["profile"] = profile
            kwargs["user_id"] = str(user.get_external_id())

            set_lastlogin_for_user_id(user.pk)

            logger.debug(
                f"IP - {request.META.get('REMOTE_ADDR', '')}, "
                f"ROLE - {UserRolesType.get_string_for_type(role) if role else 'ANON'}, "
                f"PROFILE_NAME - {profile.get_profile_name() if profile else ''}, "
                f"PROFILE_PHONE - {profile.get_phone() if profile else ''}, "
                f"VERB - {func.__name__}, "
                f"APP_NAME - {request.META.get('HTTP_APPNAME', '')}, "
                f"APP_VERSION - {request.META.get('HTTP_APPVERSION', '')}, "
                f"APP_VER_CODE - {request.META.get('HTTP_APPVERSIONCODE', '')}, "
            )

            return func(*args, **kwargs)

        return wrapper

    return decorator
