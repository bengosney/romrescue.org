# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Third Party
from psycopg2.errors import UndefinedTable


class setting(models.Model):
    title = models.CharField(max_length=150)
    value = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.title}: {self.value}"

    @staticmethod
    def getValue(title, default=""):
        try:
            obj = setting.objects.get(title=title)
        except ObjectDoesNotExist:
            obj = setting(title=title, value=default)
            obj.save()
        except UndefinedTable:
            return default

        return obj.value
