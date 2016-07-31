from vanilla import DetailView, ListView, CreateView, GenericModelView
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.apps import apps

from .models import Page, ModuleList, HomePageHeader
from .forms import ContactForm

from dogs.models import Dog

import importlib

class HomePage(ListView):
    model = Page
    template_name = 'pages/home.html'
    

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['page'] = Page.objects.get(is_home_page=True)
        context['dog_list'] = Dog.objects.all()[:4]
        context['headers'] = HomePageHeader.objects.all()

        return context


class DetailFormView(GenericModelView):
    success_url = None
    template_name_suffix = '_form'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = None
        success_message = None

        if 'success' in self.kwargs:
            success_message = self.object.success_message or 'Thank you for your submission'
        else:
            form = self.get_form()

        context = self.get_context_data(form=form, success_message=success_message)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(data=request.POST, files=request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_form_class(self):
        object = self.get_object()
        if object.form:
            self.form_class = object.getFormClass()

        return self.form_class

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        try:
            return cls(data=data, files=files, **kwargs)
        except:
            return None

    def get_success_url(self):
        object = self.get_object()
        
        return object.success_url


class PageView(DetailFormView):
    model = Page
    template_name = 'pages/index.html'
    lookup_field = 'slug'
    form_class = None


class ContactView(CreateView):
    model = Page
    template_name = 'pages/contact.html'


class ModuleListView(DetailView):
    model = ModuleList
    base_model = ModuleList
    lookup_field = 'slug'
    template_name = 'pages/modulelist.html'
 
    def get_context_data(self, **kwargs):
        raw_string = 'dogs:AdoptionList'
        app_name, view_name = raw_string.split(':')
        view_module = __import__(app_name)
        view_class = getattr(view_module.views, view_name)

        context = super(self.__class__, self).get_context_data(**kwargs)
        context['list_html'] = view_class.as_view()(self.request).rendered_content

        return context

