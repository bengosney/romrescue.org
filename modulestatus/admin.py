from django.contrib import admin

class statusAdmin(object):
    def get_queryset(self, request):
        qs = self.model.admin_objects.get_queryset()

        ordering = self.ordering or () 
        if ordering:
            qs = qs.order_by(*ordering)

        return qs
