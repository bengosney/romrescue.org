from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . import models


class AdoptionFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.AdoptionFAQ

admin.site.register(models.AdoptionFAQ, AdoptionFAQAdmin)


class FosteringFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.FosteringFAQ

admin.site.register(models.FosteringFAQ, FosteringFAQAdmin)
