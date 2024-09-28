import logging

from common.constants import ModuleErrorPrefix
from common.base_error_codes import BaseErrorCode
from rest_framework import status

logger = logging.getLogger(__name__)

class ErrorCode(BaseErrorCode):
    # Value Errors
    # (There are no value errors in geodb)

    # Permission Errors
    # (Can't have permission errors if you have no permission model)

    # Key Errors
    # What keys?

    # Object Does Not Exist Errors
    OBJECT_NOT_FOUND = 301

    # Integrity Errors

    ERROR_CODE_HTTP_MAP = {
        OBJECT_NOT_FOUND: status.HTTP_400_BAD_REQUEST,
    }

    def get_string_for_object_not_found(kwargs: dict):
        return "Object not found"

    CODE_MESSAGE_MAP = {
        OBJECT_NOT_FOUND: get_string_for_object_not_found,
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
            ModuleErrorPrefix.JWT_AUTH,
        )

