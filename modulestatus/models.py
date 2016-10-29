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


try:
    from polymorphic_tree.models import PolymorphicMPTTModel
    from polymorphic_tree.managers import PolymorphicMPTTModelManager
    from .managers import PolymorphicMPTTStatusManager

    class PolymorphicMPTTStatusModel(PolymorphicMPTTModel):
        status = models.IntegerField(
            choices=ModelStatus.STATUS_CHOICES,
            default=ModelStatus.LIVE_STATUS
        )

        _default_manager = PolymorphicMPTTStatusManager()
        admin_objects = PolymorphicMPTTModelManager()

        class Meta:
            abstract = True

except ImportError:
    pass
