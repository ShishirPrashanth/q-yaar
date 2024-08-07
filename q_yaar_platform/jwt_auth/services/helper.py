import logging
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from account.models import PlatformUser
from account.services.interfacer import (
    svc_account_check_if_user_with_email_exists,
    svc_account_create_platform_user,
    svc_account_get_platform_user_by_email,
    svc_account_get_platform_user_by_id,
    svc_account_get_serialized_platform_user,
)
from common.phonenumber import is_valid_indian_number
from jwt_auth.authentication import RefreshJSONWebToken
from jwt_auth.settings import api_settings

from .error_codes import ErrorCode


logger = logging.getLogger(__name__)


######################################################################################################################
##########################################   PRIVATE FUNCTIONS   #####################################################
######################################################################################################################


def _svc_run_basic_user_validations(request_data: dict):
    logger.debug(">>")  # Not logging locals since password will get logged

    if not request_data.get("email"):
        return ErrorCode(ErrorCode.MISSING_EMAIL)

    if not request_data.get("password"):
        return ErrorCode(ErrorCode.MISSING_PASSWORD)

    return None


def _svc_validate_email(email: str):
    logger.debug(f">> ARGS: {locals()}")

    try:
        validate_email(email)
    except ValidationError:
        return ErrorCode(ErrorCode.INVALID_EMAIL, email=email)

    return None


######################################################################################################################
########################################   PRIVATE FUNCTIONS END   ###################################################
######################################################################################################################


def svc_auth_helper_run_validations_to_get_token(request_data: dict):
    logger.debug(">>")  # Not logging locals since password will get logged

    return _svc_run_basic_user_validations(request_data=request_data)


def svc_auth_helper_run_validations_to_create_user(request_data: dict):
    logger.debug(">>")  # Not logging locals since password will get logged

    error = _svc_run_basic_user_validations(request_data=request_data)
    if error:
        return error

    error = _svc_validate_email(email=request_data["email"])
    if error:
        return error

    if not request_data.get("confirm_password"):
        return ErrorCode(ErrorCode.MISSING_CONFIRM_PASSWORD)

    if request_data["password"] != request_data["confirm_password"]:
        return ErrorCode(ErrorCode.PASSWORDS_DO_NOT_MATCH)

    return None


def svc_auth_helper_run_validations_to_check_user_exists(request_data: dict):
    logger.debug(f">> ARGS: {locals()}")

    if not request_data.get("email"):
        return ErrorCode(ErrorCode.MISSING_EMAIL)

    return None


def svc_auth_helper_run_validations_to_refresh_token(request_data: dict):
    logger.debug(f">> ARGS: {locals()}")

    if not request_data.get("token"):
        return ErrorCode(ErrorCode.MISSING_TOKEN)

    if not request_data.get("user_id"):
        return ErrorCode(ErrorCode.MISSING_USER_ID)

    return None


def svc_auth_helper_validate_and_get_user_from_email(email: str):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_get_platform_user_by_email(email=email)


def svc_auth_helper_validate_and_get_user_by_id(user_id: uuid.UUID):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_get_platform_user_by_id(user_id=user_id)


def svc_auth_helper_check_account_is_active(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    if not platform_user.is_active:
        return ErrorCode(ErrorCode.ACCOUNT_DEACTIVATED)

    if platform_user.is_suspended:
        return ErrorCode(ErrorCode.ACCOUNT_SUSPENDED)

    if platform_user.is_deleted:
        return ErrorCode(ErrorCode.ACCOUNT_DELETED)

    return None


def svc_auth_helper_check_password_for_user(platform_user: PlatformUser, password: str):
    logger.debug(">>")  # Not logging locals since password will get logged

    if not platform_user.check_password(password):
        return ErrorCode(ErrorCode.INVALID_PASSWORD)

    return None


def svc_auth_helper_get_user_token_for_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(platform_user, None, platform_user.is_suspended, None)
    jwt_token = jwt_encode_handler(payload)

    return jwt_token


def svc_auth_helper_get_serialized_jwt_token(jwt_token: str, platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return {"token": jwt_token, "user": svc_account_get_serialized_platform_user(platform_user=platform_user)}


def svc_auth_helper_validate_and_get_phone_number(phone: str):
    logger.debug(f">> ARGS: {locals()}")

    is_valid, parsed_e164, phone_number = is_valid_indian_number(mob_num=phone)

    if not is_valid:
        return ErrorCode(ErrorCode.INVALID_PHONE, phone=phone), None

    return None, parsed_e164


def svc_auth_helper_create_new_user(email: str, password: str, phone: str = None):
    logger.debug(">>")  # Not logging locals since password will get logged

    return svc_account_create_platform_user(email=email, password=password, phone=phone)


def svc_auth_helper_get_serialized_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_get_serialized_platform_user(platform_user=platform_user)


def svc_auth_helper_check_user_exists(email: str):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_check_if_user_with_email_exists(email=email)


def svc_auth_helper_get_serialized_user_exists(user_exists: bool):
    logger.debug(f">> ARGS: {locals()}")

    return {"user_exists": user_exists}


def svc_auth_helper_get_token_and_user_for_token_refresh(jwt_token: str, platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    try:
        jwt_token, user = RefreshJSONWebToken().validate_and_refresh_token(token=jwt_token, user=platform_user)
    except ValueError as e:
        return ErrorCode(ErrorCode.TOKEN_REFRESH_FAILED, error=str(e)), None, None

    return None, jwt_token, user


def svc_auth_helper_get_serialized_refresh_token(jwt_token: str, platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return {
        "user": svc_auth_helper_get_serialized_jwt_token(jwt_token=jwt_token, platform_user=platform_user),
        # "profile": svc_profile_get_token_info_all_profiles(user),
    }
