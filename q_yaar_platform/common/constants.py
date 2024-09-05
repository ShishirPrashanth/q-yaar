import enum


class BaseIntEnum(enum.IntEnum):
    @classmethod
    def tokentype_from_string(cls, token_type: str) -> "BaseIntEnum":
        """
        Override if call caps standard names won't work

        throws: KeyError for invalid token_type
        """
        return cls.__members__[token_type]

    @classmethod
    def get_string_for_type(cls, token_type: "BaseIntEnum") -> str:
        """
        Override if call caps standard names won't work

        throws: AttributeError if invalid token_type passed
        """

        return token_type.name

    @classmethod
    def get_choices(cls) -> list[tuple]:
        """
        To be used as choices field in model definition
        """
        return [(member.value, member.name) for member in cls]


class Length:
    USER_NAME = 32
    PHONE_NUMBER = 14
    GAME_CODE = 8
    TEAM_NAME = 32


class ModuleErrorPrefix:
    JWT_AUTH = "AUTH"
    ACCOUNT = "ACC"
    PROFILE_PLAYER = "PLYR"


class UserRolesType(BaseIntEnum):
    PLAYER = 1


class GameStatus(BaseIntEnum):
    CREATED = 1  # Initial game status during object creation
    LOCKED = 2  # Game not yet started but no more players allowed to join. Game config can still be changed
    IN_PROGRESS = 3  # Game has started, no more changes to game config
    COMPLETE = 4  # Game over. The game object is immutable from now.

    ABANDONED = 99  # 1. Game never started 2. Game abandoned in the middle of the game
