from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

from modulestatus.admin import statusAdmin

import json
import os

from . import models


class DogPhotoInline(
        SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.DogPhoto
    extra = 3


class KeyPointsAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.KeyPoints

    def get_querysety(self, request):
        qs = self.model.admin_objects.get_queryset()

        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)

        return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "icon":
            data_path = os.path.join(
                os.path.dirname(
                    os.path.realpath(__file__)),
                '../icons/icons.json')
            with open(data_path) as data_file:
                data = json.load(data_file)

            kwargs['choices'] = [(icon, icon) for icon in data['icons']]

        return super(
            KeyPointsAdmin,
            self).formfield_for_choice_field(
            db_field,
            request,
            **kwargs)


class DogAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.Dog
    inlines = [DogPhotoInline]
    filter_horizontal = ('keypoints',)
    list_display = ('name', 'reserved', 'location', 'dogStatus')
    list_per_page = 25

    def __init__(self, model, admin_site):
        super(DogAdmin, self).__init__(model, admin_site)

        self.list_filter = ['dogStatus', 'reserved', 'location'] + list(self.list_filter)


class StatusAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.Status


class DogPhoto(ImageCroppingMixin, admin.ModelAdmin):
    model = models.DogPhoto


class RescueAdmin(admin.ModelAdmin):
    model = models.Rescue
    list_display = ('name', 'logo', 'website')
    list_per_page = 25
    
    
admin.site.register(models.KeyPoints, KeyPointsAdmin)
admin.site.register(models.Dog, DogAdmin)
admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.Rescue, RescueAdmin)
