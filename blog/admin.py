from django.contrib import admin
from modulestatus.admin import statusAdmin

from . import models

class BlogAdmin(statusAdmin, admin.ModelAdmin):
    model = models.Blog


admin.site.register(models.Blog, BlogAdmin)
