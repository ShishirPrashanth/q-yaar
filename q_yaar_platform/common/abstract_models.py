"""
Base behaviours. Can be inherited by other models.
"""

from uuid import UUID

from django.db import models

from common.uuid import unique_uuid4


class AbstractExternalFacing(models.Model):
    """
    Used by classes to implement uuid as unique field. This is helpful for -
    1. Use external_id as external facing IDs shared with clients. Great as we will not leak information about models
     that would have happened with auto increment integer PK
    2. As FKs when we want to decouple apps into Microservices in future
    """

    external_id = models.UUIDField(default=unique_uuid4, unique=True)

    class Meta:
        abstract = True

    def get_external_id(self, hex=False) -> UUID | str:
        return self.external_id.hex if hex else self.external_id


class AbstractTimeStamped(models.Model):
    """
    Provides created and updated time fields
    """

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True
