from django.shortcuts import render
from pages.decorators import register_list_view
from .models import competition, category, submission
from .forms import SubmissionForm
from vanilla import DetailView, ListView, CreateView

@register_list_view
class CompitionList(ListView):
    model = competition
    template_name = 'photocomp/list.html'


class CompitionDetail(DetailView):
    model = competition
    template_name = 'photocomp/details.html'
    lookup_field = 'slug'


class CategoryDetails(DetailView):
    model = category
    template_name = 'photocomp/category.html'
    lookup_field = 'slug'


class CategorySubmission(CreateView):
    form_class = SubmissionForm
    models = category
    template_name = 'potocomp/submission.html'
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super(self.__class__, self).get(request, args, kwargs)
