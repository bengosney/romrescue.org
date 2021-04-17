# Future

# Django
from django.db import models

# First Party
from modulestatus import ModelStatus
from modulestatus.managers import statusManager


class statusMixin(models.Model):
    status = models.IntegerField(choices=ModelStatus.STATUS_CHOICES, default=ModelStatus.LIVE_STATUS)

    objects = statusManager()
    admin_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.status
