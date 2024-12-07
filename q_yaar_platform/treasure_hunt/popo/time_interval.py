from dataclasses import dataclass

from common.popo import PopoBase


@dataclass(init=True, repr=True, eq=False)
class TimeIntervalConfig(PopoBase):
    _from: int  # epoch timestamp
    _to: int  # epoch timestamp

    @classmethod
    def from_json(cls, config: dict) -> "TimeIntervalConfig":
        if not config:
            return cls.default()
        return cls(_from=config.get("from"), _to=config.get("to"))

    def to_json(self) -> dict:
        return {"from": self._from, "to": self._to}


@dataclass(init=True, repr=True, eq=False)
class TimeIntervalListConfig(PopoBase):
    _intervals: list[TimeIntervalConfig]

    @classmethod
    def from_json(cls, config: list[dict]) -> "TimeIntervalListConfig":
        if not config:
            return cls.default()
        return cls(_intervals=[TimeIntervalConfig.from_json(x) for x in config])

    def to_json(self) -> list[dict]:
        return [x.to_json() for x in self._intervals]
