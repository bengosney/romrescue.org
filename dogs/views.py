from django.shortcuts import render
from vanilla import DetailView, ListView, CreateView
from .models import Dog


class AdoptionList(ListView):
    model = Dog
    template_name = 'dogs/list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(status=Dog.STATUS_LOOKING)


class DogDetail(DetailView):
    model = Dog
    template_name = 'dogs/details.html'
    lookup_field = 'slug'


class SuccessDogDetail(DetailView):
    model = Dog
    template_name = 'dogs/success_details.html'
    lookup_field = 'slug'


class SuccessList(ListView):
    model = Dog
    template_name = 'dogs/success_list.html'

    def get_queryset(self):
        return self.model._default_manager.filter(status=Dog.STATUS_SUCCESS)
