# Django
from django.db import models

# First Party
from modulestatus import ModelStatus


class statusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


try:
    # Third Party
    from polymorphic_tree.managers import PolymorphicMPTTModelManager

    class PolymorphicMPTTStatusManager(PolymorphicMPTTModelManager):
        def get_queryset(self):
            return super().get_queryset().filter(status=ModelStatus.LIVE_STATUS)


except ImportError:
    pass
