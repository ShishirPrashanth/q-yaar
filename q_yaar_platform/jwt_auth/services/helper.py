import logging
import jwt

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction

from account.api.serializers import PlatformUserSerializer
from account.models import PlatformUser
from common.datetime import n_days_later
from common.phonenumber import is_valid_indian_number

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


def _svc_get_serialized_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return PlatformUserSerializer(platform_user, many=False).data


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


def svc_auth_helper_validate_and_get_user_from_email(email: str):
    logger.debug(f">> ARGS: {locals()}")

    try:
        return None, PlatformUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return ErrorCode(ErrorCode.USER_WITH_EMAIL_DOES_NOT_EXIST, email=email), None


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


def svc_auth_helper_get_user_token_for_profile(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    payload = {"user_id": str(platform_user.get_external_id()), "exp": n_days_later(settings.TOKEN_EXPIRY_DAYS)}

    jwt_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token


def svc_auth_helper_get_serialized_jwt_token(jwt_token: str, platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return {"token": jwt_token, "user": _svc_get_serialized_platform_user(platform_user=platform_user)}


def svc_auth_helper_validate_and_get_phone_number(phone: str):
    logger.debug(f">> ARGS: {locals()}")

    is_valid, parsed_e164, phone_number = is_valid_indian_number(mob_num=phone)

    if not is_valid:
        return ErrorCode(ErrorCode.INVALID_PHONE, phone=phone), None

    return None, parsed_e164


def svc_auth_helper_create_new_user(email: str, password: str, phone: str = None):
    logger.debug(">>")  # Not logging locals since password will get logged

    with transaction.atomic():
        try:
            platform_user = PlatformUser.create(email=email, phone=phone)
            platform_user.set_password(password)
            platform_user.save()
        except IntegrityError:
            return ErrorCode(ErrorCode.USER_WITH_EMAIL_ALREADY_EXISTS, email=email), None

    return None, platform_user


def svc_auth_helper_get_serialized_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return _svc_get_serialized_platform_user(platform_user=platform_user)


def svc_auth_helper_check_user_exists(email: str):
    logger.debug(f">> ARGS: {locals()}")

    return PlatformUser.objects.filter(email=email).exists()


def svc_auth_helper_get_serialized_user_exists(user_exists: bool):
    logger.debug(f">> ARGS: {locals()}")

    return {"user_exists": user_exists}
