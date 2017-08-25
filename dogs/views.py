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
