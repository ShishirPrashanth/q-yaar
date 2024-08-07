import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from account.api.serializers import PlatformUserSerializer
from account.models import PlatformUser
from .error_codes import ErrorCode


logger = logging.getLogger(__name__)


def svc_account_helper_get_platform_user_by_id(user_id: uuid.UUID):
    logger.debug(f">> ARGS: {locals()}")

    try:
        return None, PlatformUser.objects.get(external_id=user_id)
    except ObjectDoesNotExist:
        return ErrorCode(ErrorCode.INVALID_USER_ID, user_id=str(user_id)), None


def svc_account_helper_get_platform_user_by_email(email: str):
    logger.debug(f">> ARGS: {locals()}")

    try:
        return None, PlatformUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return ErrorCode(ErrorCode.INVALID_USER_EMAIL, email=email), None


def svc_account_helper_get_serialized_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    return PlatformUserSerializer(platform_user, many=False).data


def svc_account_helper_create_platform_user(email: str, password: str, phone: str = None):
    logger.debug(">>")  # Not logging locals since password will get logged

    with transaction.atomic():
        try:
            platform_user = PlatformUser.create(email=email, phone=phone)
            platform_user.set_password(password)
            platform_user.save()
        except IntegrityError:
            return ErrorCode(ErrorCode.USER_WITH_EMAIL_ALREADY_EXISTS, email=email), None

    return None, platform_user


def svc_account_helper_check_if_user_with_email_exists(email: str):
    logger.debug(f">> ARGS: {locals()}")

    return PlatformUser.objects.filter(email=email).exists()
