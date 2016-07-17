from __future__ import unicode_literals

from django.db import models

class BaseFAQ(models.Model):
    question = models.CharField(max_length=150)
    answer = models.CharField(max_length=500)
    position = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __unicode__(self):
        return self.strapline

    class Meta(object):
        ordering = ('position',)


class AdoptionFAQ(BaseFAQ):
    pass

class FosteringFAQ(BaseFAQ):
    pass
