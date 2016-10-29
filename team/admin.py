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


admin.site.register(models.TeamMember, TeamMemberAdmin)
