from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin
from image_cropping import ImageCroppingMixin

from . import models


class TeamMemberAdmin(
        SortableAdminMixin,
        ImageCroppingMixin,
        admin.ModelAdmin):
    model = models.TeamMember
    list_display = ('admin_image', 'name')
    
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

admin.site.register(models.TeamMember, TeamMemberAdmin)
