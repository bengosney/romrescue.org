# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from solo.admin import SingletonModelAdmin

# First Party
from donate.models import DontateSettings, Values


class ValuesAdmin(SortableInlineAdminMixin, admin.TabularInline):
    model = Values


@admin.register(DontateSettings)
class DontateSettingsAdmin(SortableAdminBase, SingletonModelAdmin):
    model = DontateSettings
    inlines = [ValuesAdmin]
