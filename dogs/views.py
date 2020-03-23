from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponseGone
from vanilla import DetailView, ListView
from .models import Dog, Filter
from pages.decorators import register_list_view

from rest_framework import viewsets
from .serializers import DogSerializer


@register_list_view
class AdoptionList(ListView):
    model = Dog
    template_name = 'dogs/list.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['filters'] = Filter.objects.all()

        return context

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING).order_by('reserved', 'hold', 'position')


@register_list_view
class AdoptionOldieList(ListView):
    model = Dog
    template_name = 'dogs/list_oldies.html'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING, oldie=True).order_by('reserved', 'position')


@register_list_view
class SponsorList(ListView):
    model = Dog
    template_name = 'dogs/sponsor_list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SPONSOR).order_by('reserved', 'position')


class SponsorDetail(DetailView):
    model = Dog
    template_name = 'dogs/sponsor_details.html'
    lookup_field = 'slug'


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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if self.object.dogStatus != Dog.STATUS_LOOKING:
            status_code = 410
            context['dog_list'] = Dog.objects.filter(dogStatus=Dog.STATUS_LOOKING).order_by('reserved', 'position')[:4]
            self.template_name = 'dogs/410.html'
        else:
            status_code = 200

        response = self.render_to_response(context)

        response.status_code = status_code

        return response

    def get_querysety(self):
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


class DogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Dog.objects.filter(dogStatus=Dog.STATUS_LOOKING, reserved=False).order_by('reserved', 'position')
    serializer_class = DogSerializer
