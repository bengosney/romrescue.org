from django.contrib import admin

from . import models


class SettingAdmin(admin.ModelAdmin):
    model = models.setting
    list_display = ('title', 'value')
    list_per_page = 25


admin.site.register(models.setting, SettingAdmin)
