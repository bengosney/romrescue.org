# Standard Library
import json
import os

# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from image_cropping import ImageCroppingMixin

# First Party
from modulestatus.admin import statusAdmin
from romrescue.actions import export_as_csv_action

# Locals
from . import models


class DogPhotoInline(SortableInlineAdminMixin, ImageCroppingMixin, admin.TabularInline):
    model = models.DogPhoto
    extra = 3


class YoutubeInline(SortableInlineAdminMixin, ImageCroppingMixin, admin.TabularInline):
    model = models.YoutubeVideo
    extra = 1


class AboutInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.AboutInfo
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

def make_tag_action(tag):
    def tag_action(modeladmin, request, queryset):
        for dog in queryset:
            dog.filters.add(tag)

    tag_action.short_description = "Tag dog with {0}".format(tag.name)
    tag_action.__name__ = "tag_dog_with_{0}".format(tag.slug)

    return tag_action


def make_status_action(status, name):
    def status_action(modeladmin, request, queryset):
        queryset.update(dogStatus=status)

    status_action.short_description = "Change status to {0}".format(name)
    status_action.__name__ = "change_status_to_{0}".format(status)

    return status_action


def set_price_to_default(modeladmin, request, queryset):
    queryset.update(cost=models.Dog.DEFAULT_COST)


class DogAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.Dog
    inlines = [AboutInline, DogPhotoInline, YoutubeInline]
    filter_horizontal = ('keypoints',)
    list_display = ('name', 'reserved', 'location', 'dogStatus', 'all_filters')
    list_per_page = 25
    actions = ['add_tag_dog', set_price_to_default]

    def __init__(self, model, admin_site):
        super(DogAdmin, self).__init__(model, admin_site)

        self.list_filter = ['dogStatus', 'reserved', 'location', 'promoted', 'filters', 'rescue'] + list(self.list_filter)

    def get_actions(self, request):
        actions = super(DogAdmin, self).get_actions(request)

        for tag in models.Filter.objects.all():
            action = make_tag_action(tag)
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        for status in models.Dog.STATUS:
            action = make_status_action(status[0], status[1])
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        return actions

    class Media:
        css = {
                "screen": ("/static/pages/css/admin.css",)
            }


class StatusAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.Status
    list_display = ('title', 'show_arrival_date')


class DogPhoto(ImageCroppingMixin, admin.ModelAdmin):
    model = models.DogPhoto


class RescueAdmin(admin.ModelAdmin):
    model = models.Rescue
    list_display = ('name', 'logo', 'website')
    list_per_page = 25


class FilterAdmin(admin.ModelAdmin):
    model = models.Filter


class SponsorshipInfoLinksAdmin(admin.ModelAdmin):
    model = models.SponsorshipInfoLink
    list_display = ('title', 'link', 'file')


class SponsorAdmin(admin.ModelAdmin):
    model = models.SponsorSubmission

    readonly_fields = ('created',)
    list_filter = ('created',)
    list_display = ('name', 'email', 'dog', 'created',)
    list_per_page = 25

    actions = [export_as_csv_action("CSV Export", fields=['name', 'email', 'created', 'enquiry'])]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SponsorLevelAdmin(admin.ModelAdmin):
    models = models.SponsorshipLevel

    list_display = ('name', 'cost',)


admin.site.register(models.KeyPoints, KeyPointsAdmin)
admin.site.register(models.Dog, DogAdmin)
admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.Rescue, RescueAdmin)
admin.site.register(models.Filter, FilterAdmin)
admin.site.register(models.SponsorshipInfoLink, SponsorshipInfoLinksAdmin)
admin.site.register(models.SponsorSubmission, SponsorAdmin)
admin.site.register(models.SponsorshipLevel, SponsorLevelAdmin)
