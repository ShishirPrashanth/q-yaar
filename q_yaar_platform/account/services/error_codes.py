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
    INVALID_USER_ID = "301"
    INVALID_USER_EMAIL = "302"

    # Integrity Errors - 4 Series

    ERROR_CODE_HTTP_MAP = {
        INVALID_USER_ID: status.HTTP_400_BAD_REQUEST,
        INVALID_USER_EMAIL: status.HTTP_400_BAD_REQUEST,
    }

    def get_string_for_invalid_user_id(kwargs: dict):
        return f"Invalid user_id - {kwargs.get('user_id')}"

    def get_string_for_invalid_email(kwargs: dict):
        return f"Invalid email - {kwargs.get('email')}"

    CODE_MESSAGE_MAP = {
        INVALID_USER_ID: get_string_for_invalid_user_id,
        INVALID_USER_EMAIL: get_string_for_invalid_email,
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
            ModuleErrorPrefix.ACCOUNT,
        )
