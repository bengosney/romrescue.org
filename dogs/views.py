from django.core.exceptions import MultipleObjectsReturned
from vanilla import DetailView, ListView
from .models import Dog
from pages.decorators import register_list_view


@register_list_view
class AdoptionList(ListView):
    model = Dog
    template_name = 'dogs/list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING, oldie=False).order_by('reserved', 'position')


@register_list_view
class AdoptionOldieList(ListView):
    model = Dog
    template_name = 'dogs/list_oldies.html'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING, oldie=True).order_by('reserved', 'position')


class DogDetail(DetailView):
    model = Dog
    template_name = 'dogs/details.html'
    lookup_field = 'slug'

    def get_object(self):
        try:
            return super(DogDetail, self).get_object()
        except MultipleObjectsReturned:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            objects = self.get_queryset().filter(**lookup)
            Dog._meta.get_field('slug').overwrite = True
            for obj in objects[1:]:
                obj.save()

            return objects[0]

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING)
    

class SuccessDogDetail(DetailView):
    model = Dog
    template_name = 'dogs/success_details.html'
    lookup_field = 'slug'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SUCCESS)


@register_list_view
class SuccessList(ListView):
    model = Dog
    template_name = 'dogs/success_list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SUCCESS)
