from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class setting(models.Model):
    title = models.CharField(max_length=150)
    value = models.CharField(max_length=150)

    def __str__(self):
        return "{}: {}".format(self.title, self.value)

    @staticmethod
    def getValue(title, default=""):
        try:
            obj = setting.objects.get(title=title)
        except ObjectDoesNotExist:
            obj = setting(title=title, value=default)
            obj.save()

        return obj.value
