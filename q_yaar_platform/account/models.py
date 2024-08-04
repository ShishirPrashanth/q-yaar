from django.db import models

from common.abstract_models import AbstractExternalFacing, AbstractTimeStamped
from common.constants import Length


class Player(AbstractExternalFacing, AbstractTimeStamped):
    user_name = models.CharField(max_length=Length.USER_NAME)
