from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

from modulestatus.admin import statusAdmin

from . import models

class categoryInlineAdmin(
        SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.category
    extra = 3


class competitionAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.competition
    inlines = [categoryInlineAdmin]
    list_display = ('title',)



admin.site.register(models.competition, competitionAdmin)
