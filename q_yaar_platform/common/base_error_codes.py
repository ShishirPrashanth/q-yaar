from rest_framework import status


class BaseErrorCode:
    # Success - 9 Series
    SUCCESS = "900"
    CREATED = "901"
    NO_CONTENT = "902"

    # Unhandled/unspecified error - 8 series
    SOMETHING_WENT_WRONG = "800"
    # Adding more error codes here will require changes in response.py and all error_codes constructors

    ERROR_CODE_HTTP_MAP = {
        SUCCESS: status.HTTP_200_OK,
        CREATED: status.HTTP_201_CREATED,
        NO_CONTENT: status.HTTP_204_NO_CONTENT,
        SOMETHING_WENT_WRONG: status.HTTP_400_BAD_REQUEST,
    }

    def get_string_for_something_went_wrong(kwargs: dict):
        return "Something went wrong"

    CODE_MESSAGE_MAP = {SOMETHING_WENT_WRONG: get_string_for_something_went_wrong}

    def __init__(self, code: str, http_status_code: int, message: str, module_prefix: str, **kwargs) -> None:
        self._module_prefix = module_prefix
        self.code = code
        self.http_status_code = http_status_code
        self._message = message

    def to_json(self):
        return {"code": self._module_prefix + self.code, "message": self._message}
