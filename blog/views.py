from django.shortcuts import render

from vanilla import DetailView, ListView
from .models import Blog
from pages.decorators import register_list_view


@register_list_view
class BlogList(ListView):
    model = Blog
    template_name = 'blog/list.html'

    # def get_queryset(self):
    #     return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING)


class BlogDetail(DetailView):
    model = Blog
    template_name = 'blog/details.html'
    lookup_field = 'slug'
