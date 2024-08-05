from datetime import date, datetime, timedelta

from django.utils import timezone


def local_current_datetime_from_active_tz():
    return timezone.localtime(timezone.now())


def n_days_later(n: int):
    return local_current_datetime_from_active_tz() + timezone.timedelta(days=n)
