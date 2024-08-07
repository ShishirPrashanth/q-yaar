import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from account.models import PlatformUser
from profile_player.api.serializers import PlayerProfileSerializer
from profile_player.models import PlayerProfile
from .error_codes import ErrorCode


logger = logging.getLogger(__name__)


def svc_player_helper_get_player_for_platform_user(platform_user: PlatformUser):
    logger.debug(f">> ARGS: {locals()}")

    try:
        return None, PlayerProfile.objects.get(platform_user=platform_user)
    except ObjectDoesNotExist:
        return ErrorCode(ErrorCode.PLAYER_DOES_NOT_EXIST, user_id=str(platform_user.get_external_id())), None


def svc_player_helper_get_serialized_player(player: PlayerProfile):
    logger.debug(f">> ARGS: {locals()}")

    return PlayerProfileSerializer(player, many=False).data


def svc_player_helper_create_player(
    platform_user: PlatformUser, profile_name: str, profile_pic: dict = {}, serialized: bool = False
):
    logger.debug(f">> ARGS: {locals()}")

    try:
        player = PlayerProfile.create(platform_user=platform_user, profile_name=profile_name, profile_pic=profile_pic)
    except IntegrityError:
        return ErrorCode(ErrorCode.PLAYER_ALREADY_ONBOARDED, user_id=str(platform_user.get_external_id())), None

    if serialized:
        player = svc_player_helper_get_serialized_player(player=player)

    return None, player
