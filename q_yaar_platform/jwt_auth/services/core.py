import logging

from .error_codes import ErrorCode
from .helper import (
    svc_auth_helper_check_account_is_active,
    svc_auth_helper_check_password_for_user,
    svc_auth_helper_check_user_exists,
    svc_auth_helper_create_new_user,
    svc_auth_helper_get_serialized_jwt_token,
    svc_auth_helper_get_serialized_platform_user,
    svc_auth_helper_get_serialized_refresh_token,
    svc_auth_helper_get_serialized_user_exists,
    svc_auth_helper_get_token_and_user_for_token_refresh,
    svc_auth_helper_get_user_token_for_platform_user,
    svc_auth_helper_run_validations_to_check_user_exists,
    svc_auth_helper_run_validations_to_create_user,
    svc_auth_helper_run_validations_to_get_token,
    svc_auth_helper_run_validations_to_refresh_token,
    svc_auth_helper_validate_and_get_phone_number,
    svc_auth_helper_validate_and_get_user_by_id,
    svc_auth_helper_validate_and_get_user_from_email,
)


logger = logging.getLogger(__name__)


def svc_auth_verify_password_and_get_token(request_data: dict, serialized: bool = True):
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

    token = svc_auth_helper_get_user_token_for_platform_user(platform_user=platform_user)

    if serialized:
        token = svc_auth_helper_get_serialized_jwt_token(jwt_token=token, platform_user=platform_user)

    return ErrorCode(ErrorCode.SUCCESS), token


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

    error, token, platform_user = svc_auth_helper_get_token_and_user_for_token_refresh(
        jwt_token=request_data["token"], platform_user=platform_user
    )
    if error:
        return error, None

    if serialized:
        token = svc_auth_helper_get_serialized_refresh_token(jwt_token=token, platform_user=platform_user)

    return ErrorCode(ErrorCode.SUCCESS), token
