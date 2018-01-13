from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

from modulestatus.admin import statusAdmin

import json
import os

from . import models
from . import signals

class DogPhotoInline(
        SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.DogPhoto
    extra = 3

    
class YoutubeInline(
        SortableInlineAdminMixin,
        ImageCroppingMixin,
        admin.TabularInline):
    model = models.YoutubeVideo
    extra = 1



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


def make_tag_action(tag):
    def tag_action(modeladmin, request, queryset):
        for dog in queryset:
            dog.filters.add(tag)

    tag_action.short_description = "Tag dog with {0}".format(tag.name)
    tag_action.__name__ = "tag_dog_with_{0}".format(tag.slug)

    return tag_action


class DogAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.Dog
    inlines = [DogPhotoInline, YoutubeInline]
    filter_horizontal = ('keypoints',)
    list_display = ('name', 'reserved', 'location', 'dogStatus', 'all_filters')
    list_per_page = 25
    actions = ['add_tag_dog']

    
    def __init__(self, model, admin_site):
        super(DogAdmin, self).__init__(model, admin_site)

        self.list_filter = ['dogStatus', 'reserved', 'location', 'filters', 'rescue'] + list(self.list_filter)

    def get_actions(self, request):
        actions = super(DogAdmin, self).get_actions(request)

        for tag in models.Filter.objects.all():
            action = make_tag_action(tag)
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        return actions


class StatusAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.Status


class DogPhoto(ImageCroppingMixin, admin.ModelAdmin):
    model = models.DogPhoto


class RescueAdmin(admin.ModelAdmin):
    model = models.Rescue
    list_display = ('name', 'logo', 'website')
    list_per_page = 25


class FilterAdmin(admin.ModelAdmin):
    model = models.Filter

    
admin.site.register(models.KeyPoints, KeyPointsAdmin)
admin.site.register(models.Dog, DogAdmin)
admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.Rescue, RescueAdmin)
admin.site.register(models.Filter, FilterAdmin)
