from django.conf import settings
from django.core.cache import cache

from common.datetime import local_current_datetime_from_active_tz
from .models import PlatformUser

CACHE_TTL = settings.LAST_LOGIN_CACHE_TTL


def _get_cache_key_for_user_id(user_id: int):
    return f"service.auth:{user_id}"


def set_lastlogin_for_user_id(user_id: int):
    cache_key = _get_cache_key_for_user_id(user_id)
    if cache_key not in cache:
        # we simply set 1 as a flag for existense of the key
        cache.set(cache_key, 1, timeout=CACHE_TTL)
        PlatformUser.objects.filter(pk=user_id).update(last_login=local_current_datetime_from_active_tz())
