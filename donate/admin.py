# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableInlineAdminMixin
from solo.admin import SingletonModelAdmin

# First Party
from donate.models import DontateSettings, Values


class ValuesAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = Values


class DontateSettingsAdmin(SingletonModelAdmin):
    model = DontateSettings
    inlines = [ValuesAdmin]


admin.site.register(DontateSettings, DontateSettingsAdmin)
