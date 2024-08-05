import logging

from common.constants import ModuleErrorPrefix
from common.base_error_codes import BaseErrorCode
from rest_framework import status

logger = logging.getLogger(__name__)


class ErrorCode(BaseErrorCode):
    # Value Errors - 0 Series
    MISSING_EMAIL = "001"
    MISSING_PASSWORD = "002"
    MISSING_CONFIRM_PASSWORD = "003"
    PASSWORDS_DO_NOT_MATCH = "004"
    INVALID_PHONE = "005"
    INVALID_EMAIL = "006"

    # Permission Errors - 1 Series
    ACCOUNT_DEACTIVATED = "101"
    ACCOUNT_SUSPENDED = "102"
    ACCOUNT_DELETED = "103"
    INVALID_PASSWORD = "104"

    # Key Errors - 2 Series

    # Object Does Not Exist Errors - 3 series
    USER_WITH_EMAIL_DOES_NOT_EXIST = "301"

    # Integrity Errors - 4 Series
    USER_WITH_EMAIL_ALREADY_EXISTS = "401"

    ERROR_CODE_HTTP_MAP = {
        MISSING_EMAIL: status.HTTP_400_BAD_REQUEST,
        MISSING_PASSWORD: status.HTTP_400_BAD_REQUEST,
        MISSING_CONFIRM_PASSWORD: status.HTTP_400_BAD_REQUEST,
        PASSWORDS_DO_NOT_MATCH: status.HTTP_400_BAD_REQUEST,
        INVALID_PHONE: status.HTTP_400_BAD_REQUEST,
        INVALID_EMAIL: status.HTTP_400_BAD_REQUEST,
        ACCOUNT_DEACTIVATED: status.HTTP_403_FORBIDDEN,
        ACCOUNT_SUSPENDED: status.HTTP_403_FORBIDDEN,
        ACCOUNT_DELETED: status.HTTP_403_FORBIDDEN,
        INVALID_PASSWORD: status.HTTP_401_UNAUTHORIZED,
        USER_WITH_EMAIL_DOES_NOT_EXIST: status.HTTP_400_BAD_REQUEST,
        USER_WITH_EMAIL_ALREADY_EXISTS: status.HTTP_400_BAD_REQUEST,
    }

    def get_string_for_missing_email(kwargs: dict):
        return "Missing email"

    def get_string_for_missing_password(kwargs: dict):
        return "Missing password"

    def get_string_for_missing_confirm_password(kwargs: dict):
        return "Missing confirm_password"

    def get_string_for_passwords_do_not_match(kwargs: dict):
        return "Passwords do not match"

    def get_string_for_invalid_phone(kwargs: dict):
        return f"Invalid phone number - {kwargs.get('phone')}"

    def get_string_for_invalid_email(kwargs: dict):
        return f"Invalid email id - {kwargs.get('email')}"

    def get_string_for_account_deactivated(kwargs: dict):
        return "Account not active"

    def get_string_for_account_suspended(kwargs: dict):
        return "Account has been suspended"

    def get_string_for_account_deleted(kwargs: dict):
        return "Account has been deleted"

    def get_string_for_invalid_password(kwargs: dict):
        return "Incorrect password"

    def get_string_for_user_with_email_does_not_exist(kwargs: dict):
        return f"User with email - {kwargs.get('email')} does not exist. Signup instead."

    def get_string_for_user_with_email_already_exists(kwargs: dict):
        return f"User with email - {kwargs.get('email')} already exists. Login instead."

    CODE_MESSAGE_MAP = {
        MISSING_EMAIL: get_string_for_missing_email,
        MISSING_PASSWORD: get_string_for_missing_password,
        MISSING_CONFIRM_PASSWORD: get_string_for_missing_confirm_password,
        PASSWORDS_DO_NOT_MATCH: get_string_for_passwords_do_not_match,
        INVALID_PHONE: get_string_for_invalid_phone,
        INVALID_EMAIL: get_string_for_invalid_email,
        ACCOUNT_DEACTIVATED: get_string_for_account_deactivated,
        ACCOUNT_SUSPENDED: get_string_for_account_suspended,
        ACCOUNT_DELETED: get_string_for_account_deleted,
        INVALID_PASSWORD: get_string_for_invalid_password,
        USER_WITH_EMAIL_DOES_NOT_EXIST: get_string_for_user_with_email_does_not_exist,
        USER_WITH_EMAIL_ALREADY_EXISTS: get_string_for_user_with_email_already_exists,
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
