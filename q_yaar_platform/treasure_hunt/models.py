import uuid
import pghistory

from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint

from common.abstract_models import (
    AbstractExternalFacing,
    AbstractGame,
    AbstractTeam,
    AbstractTimeStamped,
    AbstractVersioned,
)
from common.constants import GameStatus
from profile_player.models import PlayerProfile
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
    def create(
        cls, game_duration: TimeIntervalListConfig, start_timestamp: int, end_timestamp: int
    ) -> "TreasureHuntGame":  # TODO: Populate info fields
        info = {
            cls.CONST_KEY_GAME_DURATION: game_duration.to_json(),
            cls.CONST_KEY_START_TIMESTAMP: start_timestamp,
            cls.CONST_KEY_END_TIMESTAMP: end_timestamp,
        }
        treasure_hunt_game = cls(game_code=cls._generate_random_game_code(), info=info)
        treasure_hunt_game.save()
        return treasure_hunt_game


@pghistory.track()
class TreasureHuntTeam(AbstractTeam, AbstractExternalFacing, AbstractTimeStamped, AbstractVersioned):
    game = models.ForeignKey(TreasureHuntGame, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=["team_name"])]

    def __str__(self) -> str:
        return f"{self.game.game_code} - {self.team_name}"

    @classmethod
    def create(cls, team_name: str, game: TreasureHuntGame) -> "TreasureHuntTeam":
        treasure_hunt_team = cls(team_name=team_name, game=game)
        treasure_hunt_team.save()
        return treasure_hunt_team


class TreasureHuntPlayer(AbstractTimeStamped):
    player = models.ForeignKey(PlayerProfile, on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ForeignKey(TreasureHuntTeam, on_delete=models.CASCADE, blank=True, null=True, default=None)
    game = models.ForeignKey(
        TreasureHuntGame, on_delete=models.CASCADE
    )  # can get this from team.game as well but this is for when the player hasn't yet joined a team

    class Meta:
        indexes = [models.Index(fields=["player"]), models.Index(fields=["team"]), models.Index(fields=["game"])]

    @classmethod
    def create(
        cls, player: PlayerProfile, game: TreasureHuntGame, team: TreasureHuntTeam | None = None
    ) -> "TreasureHuntPlayer":
        treasure_hunt_player = cls(player=player, game=game)
        if team:
            treasure_hunt_player.team = team
        treasure_hunt_player.save()
        return treasure_hunt_player
