from dataclasses import dataclass

from common.popo import PopoBase


@dataclass(init=True, repr=True, eq=False)
class PlayerInfoConfig(PopoBase):
    _profile_name: str
    _email: str

    @classmethod
    def from_json(cls, config: dict) -> "PlayerInfoConfig":
        if not config:
            return cls.default()
        return cls(_profile_name=config.get("profile_name"), _email=config.get("email"))

    def to_json(self) -> dict:
        return {"profile_name": self._profile_name, "email": self._email}
