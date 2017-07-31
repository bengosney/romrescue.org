from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q

from . import ModelStatus


class statusManager(models.Manager):
    def get_queryset(self):
        return super(statusManager, self)\
            .get_queryset()\
            .filter(status=ModelStatus.LIVE_STATUS)

    
class statusDateManager(statusManager):
    def get_queryset(self):
        return super(statusManager, self)\
            .get_queryset()\
            .filter(published_date__gte=datetime.now()-timedelta(days=-1))
    

try:
    from polymorphic_tree.managers import PolymorphicMPTTModelManager

    class PolymorphicMPTTStatusManager(PolymorphicMPTTModelManager):
        def get_queryset(self):
            return super(PolymorphicMPTTStatusManager, self)\
                .get_queryset().filter(status=ModelStatus.LIVE_STATUS)
except ImportError:
    pass
