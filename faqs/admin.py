from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin

from . import models


class AdoptionFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.AdoptionFAQ
    
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

admin.site.register(models.AdoptionFAQ, AdoptionFAQAdmin)


class FosteringFAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    model = models.FosteringFAQ
    
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

admin.site.register(models.FosteringFAQ, FosteringFAQAdmin)
