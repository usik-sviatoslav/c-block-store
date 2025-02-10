import uuid6
from django.db import models


class UUIDv7Model(models.Model):
    """
    This abstract base class provides id field on any model that inherits from it
    which will be the primary key.
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, editable=False)  # noqa: VNE003
