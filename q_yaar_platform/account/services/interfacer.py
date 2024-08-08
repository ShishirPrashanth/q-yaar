import logging
import uuid

from account.models import PlatformUser

from .helper import (
    svc_account_helper_check_if_user_with_email_exists,
    svc_account_helper_get_or_create_platform_user,
    svc_account_helper_get_platform_user_by_email,
    svc_account_helper_get_platform_user_by_id,
    svc_account_helper_get_serialized_platform_user,
)


logger = logging.getLogger(__name__)


def svc_account_get_platform_user_by_id(user_id: uuid.UUID):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_helper_get_platform_user_by_id(user_id=user_id)


def svc_account_get_platform_user_by_email(email: str):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_helper_get_platform_user_by_email(email=email)


def svc_account_get_serialized_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return svc_account_helper_get_serialized_platform_user(platform_user=platform_user)


def svc_account_get_or_create_platform_user(email: str, password: str, phone: str = None):
    logger.debug(">>")  # Not logging locals since password will get logged

    return svc_account_helper_get_or_create_platform_user(email=email, password=password, phone=phone)


def svc_account_check_if_user_with_email_exists(email: str):
    return svc_account_helper_check_if_user_with_email_exists(email=email)
