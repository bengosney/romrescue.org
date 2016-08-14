from __future__ import unicode_literals

from django.db import models

from . import ModelStatus
from .managers import statusManager

class statusMixin(models.Model):
    status = models.IntegerField(
        choices=ModelStatus.STATUS_CHOICES,
        default=ModelStatus.LIVE_STATUS
    )

    objects = statusManager()
    admin_objects = models.Manager()

    class Meta:
        abstract = True
