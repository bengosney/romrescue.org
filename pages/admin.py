from django.contrib import admin

from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, \
    PolymorphicMPTTChildModelAdmin
from adminsortable2.admin import SortableAdminMixin
from image_cropping import ImageCroppingMixin

from .models import ContactSubmission, Page, Empty, ModuleList, \
    ExternalLink, SocialLink, node, HomePageHeader


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
        (Page, BaseChildAdmin),
        (Empty, BaseChildNoSEOAdmin),
        (ModuleList, ModuleListAdmin),
        (ExternalLink, BaseChildNoSEOAdmin),
        (SocialLink, BaseChildNoSEOAdmin),
    )

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }


class ContactAdmin(admin.ModelAdmin):
    model = ContactSubmission

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

admin.site.register(node, TreeNodeParentAdmin)
admin.site.register(ContactSubmission, ContactAdmin)
admin.site.register(HomePageHeader, HomePageHeaderAdmin)
