# Django
from django.contrib import admin

# Third Party
from adminsortable2.admin import SortableAdminMixin

# First Party
from modulestatus.admin import statusAdmin
from testimonials import models


class TestimonialAdmin(SortableAdminMixin, statusAdmin, admin.ModelAdmin):
    model = models.Testimonial


admin.site.register(models.Testimonial, TestimonialAdmin)
