# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin
from image_cropping import ImageCroppingMixin
from polymorphic_tree.admin import PolymorphicMPTTChildModelAdmin, PolymorphicMPTTParentModelAdmin

# First Party
from romrescue.actions import export_as_csv_action

# Locals
from .models import ContactSubmission, Empty, ExternalLink, HomePageHeader, IntrestSubmission, ModuleList, Page, SocialLink, node


class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'status', 'title'),
    })

    SEO_FIELDSET = ('SEO', {
        'classes': ('grp-collapse grp-closed',),
        'fields': ('title_tag', 'meta_description'),
    })

    NAV_FIELDSET = ('Navigation', {
        'classes': ('grp-collapse grp-closed',),
        'fields': ('nav_title',
                   'nav_icon',
                   'nav_icon_only',
                   'active_url_helper'),
    })

    base_model = node
    base_fieldsets = (
        GENERAL_FIELDSET,
        NAV_FIELDSET,
        SEO_FIELDSET,
    )


class BaseChildNoSEOAdmin(BaseChildAdmin):
    pass


class ModuleListAdmin(BaseChildAdmin):
    pass


class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = node
    child_models = (
        Page,
        Empty,
        ModuleList,
        ExternalLink,
        SocialLink,
    )

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }


class ContactAdmin(admin.ModelAdmin):
    model = ContactSubmission

    readonly_fields = ('created',)
    list_filter = ('created',)
    list_display = ('name', 'email', 'created',)
    list_per_page = 25

    actions = [export_as_csv_action("CSV Export", fields=['name', 'email', 'created', 'enquiry'])]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class IntrestAdmin(admin.ModelAdmin):
    model = IntrestSubmission

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class HomePageHeaderAdmin(
        SortableAdminMixin,
        ImageCroppingMixin,
        admin.ModelAdmin):
    model = HomePageHeader
    list_display = ('admin_image', 'strapline', 'subline',)

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'image_cropping/js/jquery.Jcrop.min.js',
            'adminsortable2/js/plugins/admincompat.js',
            'adminsortable2/js/libs/jquery.ui.core-1.11.4.js',
            'adminsortable2/js/libs/jquery.ui.widget-1.11.4.js',
            'adminsortable2/js/libs/jquery.ui.mouse-1.11.4.js',
            'adminsortable2/js/libs/jquery.ui.sortable-1.11.4.js',
            'adminsortable2/js/list-sortable.js',
            'adminsortable2/js/inline-sortable.js',
        )


admin.site.register(node, TreeNodeParentAdmin)
admin.site.register(ContactSubmission, ContactAdmin)
admin.site.register(IntrestSubmission, IntrestAdmin)

admin.site.register(Page, BaseChildAdmin)
admin.site.register(Empty, BaseChildNoSEOAdmin)
admin.site.register(ModuleList, ModuleListAdmin)
admin.site.register(ExternalLink, BaseChildNoSEOAdmin)
admin.site.register(SocialLink, BaseChildNoSEOAdmin)
