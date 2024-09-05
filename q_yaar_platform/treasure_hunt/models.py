import uuid
import pghistory

from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint

from common.abstract_models import AbstractExternalFacing, AbstractGame, AbstractTimeStamped, AbstractVersioned
from common.constants import GameStatus
from treasure_hunt.popo.time_interval import TimeIntervalListConfig


@pghistory.track()
class TreasureHuntGame(AbstractGame, AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned):
    CONST_KEY_GAME_DURATION = "game_duration"
    CONST_KEY_START_TIMESTAMP = "start_timestamp"  # epoch timestamp
    CONST_KEY_END_TIMESTAMP = "end_timestamp"  # epoch timestamp

    info = models.JSONField(default=dict)

    class Meta:
        indexes = [models.Index(fields=["game_code"])]
        constraints = [
            UniqueConstraint(
                fields=["game_code", "game_status"],
                condition=Q(game_status=GameStatus.CREATED.value),
                name="trasure_hunt_unique_game_code_for_created_games",
            )
        ]

    def __str__(self) -> str:
        return f"{self.game_code}"

    def get_game_duration(self) -> TimeIntervalListConfig:
        return TimeIntervalListConfig.from_json(self.info.get(self.CONST_KEY_GAME_DURATION))

    def set_game_duration(self, game_duration: TimeIntervalListConfig, save: bool = False) -> "TreasureHuntGame":
        info = self.info
        info[self.CONST_KEY_GAME_DURATION] = game_duration.to_json()
        self.info = info
        if save:
            self.save()
        return self

    def get_start_timestamp(self) -> int:
        return self.info.get(self.CONST_KEY_START_TIMESTAMP)

    def set_start_timestamp(self, start_timestamp: int, save: bool = False) -> "TreasureHuntGame":
        info = self.info
        info[self.CONST_KEY_START_TIMESTAMP] = start_timestamp
        self.info = info
        if save:
            self.save()
        return self

    def get_end_timestamp(self) -> int:
        return self.info.get(self.CONST_KEY_END_TIMESTAMP)

    def set_end_timestamp(self, end_timestamp: int, save: bool = False) -> "TreasureHuntGame":
        info = self.info
        info[self.CONST_KEY_END_TIMESTAMP] = end_timestamp
        self.info = info
        if save:
            self.save()
        return self

    @classmethod
    def _generate_random_game_code(cls):
        return str(uuid.uuid4())[: settings.GAME_CODE_LENGTH].upper()

    @classmethod
    def create(cls) -> "TreasureHuntGame":  # TODO: Populate info fields
        treasure_hunt_game = cls(game_code=cls._generate_random_game_code())
        treasure_hunt_game.save()
        return treasure_hunt_game
