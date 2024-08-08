import logging

from account.models import PlatformUser
from common.constants import UserRolesType

from .helper import svc_auth_helper_get_profile_for_user_and_role


logger = logging.getLogger(__name__)


def svc_auth_get_profile_for_user_and_role(platform_user: PlatformUser, role: UserRolesType):
    logger.debug(f">> ARGS: {locals()}")

    return svc_auth_helper_get_profile_for_user_and_role(platform_user=platform_user, role=role)
