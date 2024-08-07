from functools import wraps
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response

from common.constants import UserRolesType
# from services.profile import svc_profile_get_profile_from_request_auth
# from account.cache import set_lastlogin_for_user_id


def validate_user(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[1]

            user = request.user

            kwargs["user_id"] = str(user.get_external_id())

            logger.debug(
                f"IP - {request.META.get('REMOTE_ADDR', '')}, "
                f"USER_ID - {str(user.get_external_id())}, "
                f"USER_EMAIL - {user.email}, "
                f"USER_PHONE - {user.phone}, "
                f"VERB - {func.__name__}, "
                f"APP_NAME - {request.META.get('HTTP_APPNAME', '')}, "
                f"APP_VERSION - {request.META.get('HTTP_APPVERSION', '')}, "
                f"APP_VER_CODE - {request.META.get('HTTP_APPVERSIONCODE', '')}, "
            )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# def validate_profile(logger, allowed_roles: List[UserRolesType] = []):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             request = args[1]
#             profile, profile_suspended, role = svc_profile_get_profile_from_request_auth(request.user, request.auth)

#             if profile_suspended:
#                 return Response({"message": "Suspended Profile"}, status=status.HTTP_403_FORBIDDEN)
#             if profile and profile.platform_user.is_deleted:
#                 return Response(
#                     {"message": "User account is deleted. Please Sign up again to proceed"},
#                     status=status.HTTP_401_UNAUTHORIZED,
#                 )
#             if allowed_roles and role not in allowed_roles:
#                 return Response(
#                     {
#                         "message": (
#                             "Invalid Role. Only allowed for"
#                             f" {', '.join([role.name if role else 'GUEST' for role in allowed_roles])}"
#                         )
#                     },
#                     status=status.HTTP_403_FORBIDDEN,
#                 )

#             kwargs["role"] = role
#             kwargs["profile"] = profile
#             kwargs["user_id"] = profile.platform_user.external_id if profile else None

#             # sets last_login to now for user
#             # has a window of 15 mins
#             if profile:
#                 set_lastlogin_for_user_id(profile.platform_user.pk)

#             logger.debug(
#                 f"IP - {request.META.get('REMOTE_ADDR', '')}, "
#                 f"ROLE - {UserRolesType.get_string_for_type(role) if role else 'ANON'}, "
#                 f"PROFILE_NAME - {profile.get_profile_name() if profile else ''}, "
#                 f"PROFILE_PHONE - {profile.get_phone() if profile else ''}, "
#                 f"VERB - {func.__name__}, "
#                 f"APP_NAME - {request.META.get('HTTP_APPNAME', '')}, "
#                 f"APP_VERSION - {request.META.get('HTTP_APPVERSION', '')}, "
#                 f"APP_VER_CODE - {request.META.get('HTTP_APPVERSIONCODE', '')}, "
#             )

#             return func(*args, **kwargs)

#         return wrapper

#     return decorator
