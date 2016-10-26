from django.db import models

from . import ModelStatus

class statusManager(models.Manager):
    def get_queryset(self):
        return super(statusManager, self).get_queryset().filter(status=ModelStatus.LIVE_STATUS)


try:
    from polymorphic_tree.managers import PolymorphicMPTTModelManager

    class PolymorphicMPTTStatusManager(PolymorphicMPTTModelManager):
        def get_queryset(self):
            return super(PolymorphicMPTTStatusManager, self).get_queryset().filter(status=ModelStatus.LIVE_STATUS)
except ImportError:
    pass
