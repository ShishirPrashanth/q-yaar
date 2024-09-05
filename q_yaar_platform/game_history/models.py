import uuid

from django.db import models

from common.abstract_models import AbstractTimeStamped, AbstractVersioned
from common.constants import GameResult, GameType, Length
from profile_player.models import PlayerProfile
from profile_player.popo.player_info import PlayerInfoConfig


class PlayerGameHistory(AbstractTimeStamped, AbstractVersioned):
    CONST_KEY_PLAYER_INFO = "player_info"

    player = models.ForeignKey(PlayerProfile, on_delete=models.SET_NULL, blank=True, null=True)
    game_type = models.PositiveIntegerField(choices=GameType.get_choices())
    game_id = models.UUIDField(blank=False, null=False)
    team_name = models.CharField(max_length=Length.TEAM_NAME, blank=True, null=True, default=None)
    game_result = models.PositiveIntegerField(choices=GameResult.get_choices(), default=GameResult.NA)

    info = models.JSONField(default=dict)

    class Meta:
        indexes = [models.Index(fields=["player"])]

    @classmethod
    def create(
        cls, player: PlayerProfile, game_type: GameType, game_id: uuid.UUID, player_info: PlayerInfoConfig
    ) -> "PlayerGameHistory":
        info = {cls.CONST_KEY_PLAYER_INFO: player_info.to_json()}
        player_game_history = cls(player=player, game_type=game_type, game_id=game_id, info=info)
        player_game_history.save()
        return player_game_history
