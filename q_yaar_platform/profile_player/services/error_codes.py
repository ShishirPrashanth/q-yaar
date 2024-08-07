import logging

from common.constants import ModuleErrorPrefix
from common.base_error_codes import BaseErrorCode
from rest_framework import status

logger = logging.getLogger(__name__)


class ErrorCode(BaseErrorCode):
    # Value Errors - 0 Series

    # Permission Errors - 1 Series

    # Key Errors - 2 Series

    # Object Does Not Exist Errors - 3 series
    PLAYER_DOES_NOT_EXIST = "301"

    # Integrity Errors - 4 Series
    PLAYER_ALREADY_ONBOARDED = "401"

    ERROR_CODE_HTTP_MAP = {
        PLAYER_DOES_NOT_EXIST: status.HTTP_400_BAD_REQUEST,
        PLAYER_ALREADY_ONBOARDED: status.HTTP_400_BAD_REQUEST,
    }

    def get_string_for_player_does_not_exist(kwargs: dict):
        return f"Player profile does not exist for user id - {kwargs.get('user_id')}"

    def get_string_for_player_already_onboarded(kwargs: dict):
        return f"Player already onboarded for user id - {kwargs.get('user_id')}"

    CODE_MESSAGE_MAP = {
        PLAYER_DOES_NOT_EXIST: get_string_for_player_does_not_exist,
        PLAYER_ALREADY_ONBOARDED: get_string_for_player_already_onboarded,
    }

    def __init__(self, code, **kwargs) -> None:
        self.ERROR_CODE_HTTP_MAP.update(super(ErrorCode, self).ERROR_CODE_HTTP_MAP)
        self.CODE_MESSAGE_MAP.update(super(ErrorCode, self).CODE_MESSAGE_MAP)

        (
            logger.debug(f">> ARGS: {locals()}")
            if code in [self.SUCCESS, self.CREATED, self.NO_CONTENT]
            else logger.warning(f"{self.CODE_MESSAGE_MAP[code](kwargs)} - {locals()}")
        )

        super(ErrorCode, self).__init__(
            code,
            self.ERROR_CODE_HTTP_MAP[code],
            self.CODE_MESSAGE_MAP[code](kwargs) if code not in [self.SUCCESS, self.CREATED, self.NO_CONTENT] else None,
            ModuleErrorPrefix.PROFILE_PLAYER,
        )
