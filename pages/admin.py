# Standard Library
from datetime import datetime, timedelta

# Django
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

# Third Party
from adminsortable2.admin import SortableAdminMixin
from image_cropping import ImageCroppingMixin
from polymorphic_tree.admin import PolymorphicMPTTChildModelAdmin, PolymorphicMPTTParentModelAdmin

# First Party
from pages.models import (
    ContactSubmission,
    Empty,
    ExternalLink,
    HomePageHeader,
    IntrestSubmission,
    ModuleList,
    Page,
    SocialLink,
    node,
)
from romrescue.actions import export_as_csv_action


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    LogEntry.objects.filter(action_time__lt=(datetime.now() - timedelta(days=30))).delete()


@admin.register(Page)
class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (
        None,
        {
            "fields": ("parent", "status", "title"),
        },
    )

    SEO_FIELDSET = (
        "SEO",
        {
            "classes": ("grp-collapse grp-closed",),
            "fields": ("title_tag", "meta_description"),
        },
    )

    NAV_FIELDSET = (
        "Navigation",
        {
            "classes": ("grp-collapse grp-closed",),
            "fields": ("nav_title", "nav_icon", "nav_icon_only", "active_url_helper"),
        },
    )

    base_model = node
    base_fieldsets = (
        GENERAL_FIELDSET,
        NAV_FIELDSET,
        SEO_FIELDSET,
    )


@admin.register(Empty, ExternalLink, SocialLink)
class BaseChildNoSEOAdmin(BaseChildAdmin):
    pass


@admin.register(ModuleList)
class ModuleListAdmin(BaseChildAdmin):
    pass


@admin.register(node)
class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = node
    child_models = (
        Page,
        Empty,
        ModuleList,
        ExternalLink,
        SocialLink,
    )

    list_display = (
        "title",
        "actions_column",
    )

    class Media:
        css = {"all": ("admin/treenode/admin.css",)}


@admin.register(ContactSubmission)
class ContactAdmin(admin.ModelAdmin):
    model = ContactSubmission

    readonly_fields = ("created",)
    list_filter = ("created",)
    list_display = (
        "name",
        "email",
        "created",
    )
    list_per_page = 25

    actions = [export_as_csv_action("CSV Export", fields=["name", "email", "created", "enquiry"])]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IntrestSubmission)
class IntrestAdmin(admin.ModelAdmin):
    model = IntrestSubmission

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class HomePageHeaderAdmin(SortableAdminMixin, ImageCroppingMixin, admin.ModelAdmin):
    model = HomePageHeader
    list_display = (
        "admin_image",
        "strapline",
        "subline",
    )



