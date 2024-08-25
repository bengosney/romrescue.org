# Django
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Third Party
from vanilla import CreateView, DetailView, GenericModelView, ListView

# First Party
from dogs.models import Dog
from pages.models import HomePageHeader, IntrestSubmission, ModuleList, Page


def error404(request, exception):
    response = render(request, "pages/404.html")
    response.status_code = 404

    return response


class HomePage(ListView):
    model = Page
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context["page"] = Page.objects.get(is_home_page=True)
        context["dog_list"] = Dog.get_homepage_dogs()
        context["dog_headders"] = Dog.get_homepage_header_dogs()
        context["headers"] = HomePageHeader.objects.all()

        return context


class DetailFormView(GenericModelView):
    success_url = None
    template_name_suffix = "_form"
    base_message = "Thank you for your submission"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = None
        success_message = None

        if "success" in self.kwargs:
            success_message = self.object.success_message or self.base_message
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

        self.object.send_email()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_form_class(self):
        object = self.get_object()
        if object.form:
            self.form_class = object.get_form_class()

        return self.form_class

    def get_form(self, data=None, files=None, **kwargs):
        cls = self.get_form_class()
        try:
            return cls(data=data, files=files, **kwargs)
        except BaseException:
            return None

    def get_success_url(self):
        object = self.get_object()

        return object.success_url


class PageView(DetailFormView):
    model = Page
    template_name = "pages/index.html"
    lookup_field = "slug"
    form_class = None


class ContactView(CreateView):
    model = Page
    template_name = "pages/contact.html"


class IntrestView(CreateView):
    model = IntrestSubmission
    fields = "__all__"
    template_name = "pages/intrest.html"


class IntrestSuccessView(DetailView):
    model = IntrestSubmission
    lookup_field = "slug"
    template_name = "pages/intrest_success.html"


class ModuleListView(DetailView):
    model = ModuleList
    base_model = ModuleList
    lookup_field = "slug"
    template_name = "pages/modulelist.html"

    def get_context_data(self, **kwargs):
        view_string = self.object.module.split(".")

        view_class = __import__(view_string[0])
        for part in view_string[1:]:
            view_class = getattr(view_class, part)

        context = super(self.__class__, self).get_context_data(**kwargs)
        context["list_html"] = view_class.as_view()(self.request).rendered_content

        return context
