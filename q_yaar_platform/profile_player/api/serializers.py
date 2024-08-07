from rest_framework import serializers

from account.api.serializers import PlatformUserSerializer
from profile_player.models import PlayerProfile


class PlayerProfileSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = PlayerProfile
        fields = ("profile_name", "user_profile", "profile_pic", "created", "modified", "is_suspended")

    def get_user_profile(self, obj: PlayerProfile):
        return PlatformUserSerializer(obj.platform_user, many=False).data

    def get_profile_pic(self, obj: PlayerProfile):
        return obj.get_profile_pic()
