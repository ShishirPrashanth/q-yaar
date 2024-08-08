from rest_framework import serializers

from account.models import PlatformUser


class PlatformUserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = PlatformUser
        fields = ("user_id", "email", "phone", "is_active")

    def get_user_id(self, obj: PlatformUser):
        return str(obj.get_external_id())
