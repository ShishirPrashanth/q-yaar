import logging

from account.models import PlatformUser
from common.constants import UserRolesType
from profile_player.models import PlayerProfile

from .error_codes import ErrorCode
from .helper import (
    svc_auth_helper_check_account_is_active,
    svc_auth_helper_check_password_for_user,
    svc_auth_helper_check_user_exists,
    svc_auth_helper_create_new_user,
    svc_auth_helper_create_profile_for_user,
    svc_auth_helper_get_all_serialized_roles_for_user,
    svc_auth_helper_get_serialized_jwt_token,
    svc_auth_helper_get_serialized_platform_user,
    svc_auth_helper_get_serialized_refresh_token,
    svc_auth_helper_get_serialized_user_exists,
    svc_auth_helper_get_token_and_user_for_token_refresh,
    svc_auth_helper_get_user_token_for_platform_user,
    svc_auth_helper_run_validations_to_check_user_exists,
    svc_auth_helper_run_validations_to_create_profile,
    svc_auth_helper_run_validations_to_create_user,
    svc_auth_helper_run_validations_to_get_token,
    svc_auth_helper_run_validations_to_refresh_token,
    svc_auth_helper_update_profile,
    svc_auth_helper_validate_and_get_phone_number,
    svc_auth_helper_validate_and_get_role,
    svc_auth_helper_validate_and_get_user_by_id,
    svc_auth_helper_validate_and_get_user_from_email,
)


logger = logging.getLogger(__name__)


def svc_auth_verify_password_and_get_token(request_data: dict):
    logger.debug(">>")  # Not logging locals since password will get logged

    error = svc_auth_helper_run_validations_to_get_token(request_data=request_data)
    if error:
        return error, None

    error, platform_user = svc_auth_helper_validate_and_get_user_from_email(email=request_data["email"])
    if error:
        return error, None

    error = svc_auth_helper_check_account_is_active(platform_user=platform_user)
    if error:
        return error, None

    error = svc_auth_helper_check_password_for_user(platform_user=platform_user, password=request_data["password"])
    if error:
        return error, None

    access_token, refresh_token = svc_auth_helper_get_user_token_for_platform_user(platform_user=platform_user)

    response = svc_auth_helper_get_serialized_jwt_token(
        access_token=access_token, refresh_token=refresh_token, platform_user=platform_user
    )

    return ErrorCode(ErrorCode.SUCCESS), response


def svc_auth_create_new_user(request_data: dict, serialized: bool = True):
    logger.debug(">>")  # Not logging locals since password will get logged

    error = svc_auth_helper_run_validations_to_create_user(request_data=request_data)
    if error:
        return error, None

    phone = None
    if request_data.get("phone"):
        error, phone = svc_auth_helper_validate_and_get_phone_number(phone=request_data.get("phone"))
        if error:
            logger.warning(f"Invalid phone number entered - {request_data['phone']}")

    error, platform_user = svc_auth_helper_create_new_user(
        email=request_data["email"], password=request_data["password"], phone=phone
    )
    if error:
        return error, None

    if serialized:
        platform_user = svc_auth_helper_get_serialized_platform_user(platform_user=platform_user)

    return ErrorCode(ErrorCode.CREATED), platform_user


def svc_auth_check_user_exists(request_data: dict, serialized: bool = True):
    logger.debug(f">> ARGS: {locals()}")

    error = svc_auth_helper_run_validations_to_check_user_exists(request_data=request_data)
    if error:
        return error, None

    user_exists = svc_auth_helper_check_user_exists(request_data["email"])

    if serialized:
        user_exists = svc_auth_helper_get_serialized_user_exists(user_exists=user_exists)

    return ErrorCode(ErrorCode.SUCCESS), user_exists


def svc_auth_refresh_token(request_data: dict, serialized: bool = True):
    logger.debug(f">> ARGS: {locals()}")

    error = svc_auth_helper_run_validations_to_refresh_token(request_data=request_data)
    if error:
        return error, None

    error, platform_user = svc_auth_helper_validate_and_get_user_by_id(user_id=request_data["user_id"])
    if error:
        return error, None

    error, acccess_token, refresh_token = svc_auth_helper_get_token_and_user_for_token_refresh(
        refresh_token=request_data["refresh_token"], platform_user=platform_user
    )
    if error:
        return error, None

    response = svc_auth_helper_get_serialized_refresh_token(
        access_token=acccess_token, refresh_token=refresh_token, platform_user=platform_user
    )

    return ErrorCode(ErrorCode.SUCCESS), response


def svc_auth_get_all_profiles_for_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    profiles = svc_auth_helper_get_all_serialized_roles_for_user(platform_user=platform_user)

    return ErrorCode(ErrorCode.SUCCESS), profiles


def svc_auth_create_profile_for_user(request_data: dict, platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    error = svc_auth_helper_run_validations_to_create_profile(request_data=request_data)
    if error:
        return error, None

    error, role = svc_auth_helper_validate_and_get_role(request_data["role"])
    if error:
        return error, None

    error, serialized_profile = svc_auth_helper_create_profile_for_user(
        platform_user=platform_user,
        role=role,
        profile_name=request_data["profile_name"],
        profile_pic=request_data.get("profile_pic", {}),
    )
    if error:
        return error, None

    return ErrorCode(ErrorCode.CREATED), serialized_profile


def svc_auth_update_profile(request_data: dict, profile: PlayerProfile, role: UserRolesType, serialized: bool = True):
    logger.debug(f">> ARGS: {locals()}")

    response = svc_auth_helper_update_profile(
        request_data=request_data, profile=profile, role=role, serialized=serialized
    )

    return ErrorCode(ErrorCode.SUCCESS), response
