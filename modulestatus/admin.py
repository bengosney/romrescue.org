# from django.contrib import admin

# from . import ModelStatus


class statusAdmin(object):
    def __init__(self, model, admin_site):
        super(statusAdmin, self).__init__(model, admin_site)

        self.list_display = ['status'] + list(self.list_display)
        self.list_filter = ['status'] + list(self.list_filter)

    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)

        return qs
