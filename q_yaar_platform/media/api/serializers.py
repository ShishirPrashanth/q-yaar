from rest_framework import serializers

from common.constants import AssetStatus
from media.models import Asset
from profile_game_master.api.serializers import GameMasterProfileSerializer
from profile_game_master.models import GameMasterProfile
from profile_player.api.serializers import PlayerProfileSerializer


class AssetSerializer(serializers.ModelSerializer):
    asset_id = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = (
            "asset_id",
            "profile",
            "object_key",
            "asset_name",
            "content_type",
            "status",
            "created",
            "modified",
        )

    def get_asset_id(self, obj: Asset) -> str:
        return str(obj.get_external_id())

    def get_profile(self, obj: Asset) -> dict:
        # Set by the service layer from the request's profile (owner-scoped).
        profile = obj._uploader_profile

        if isinstance(profile, GameMasterProfile):
            return GameMasterProfileSerializer(profile, many=False).data

        return PlayerProfileSerializer(profile, many=False).data

    def get_status(self, obj: Asset) -> str:
        return AssetStatus.get_string_for_type(AssetStatus(obj.status))
