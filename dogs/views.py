# Django
from django.core.exceptions import MultipleObjectsReturned

# Third Party
from vanilla import DetailView, ListView

# First Party
from dogs.models import Dog, Filter, SponsorshipInfoLink
from pages.decorators import register_list_view
from pages.forms import SponsorForm


@register_list_view
class AdoptionList(ListView):
    model = Dog
    template_name = "dogs/list.html"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context["filters"] = Filter.objects.all()

        return context

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING).order_by(
            "reserved", "-hold_type_id", "position"
        )


@register_list_view
class AdoptionOldieList(ListView):
    model = Dog
    template_name = "dogs/list_oldies.html"

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_LOOKING, oldie=True).order_by(
            "reserved", "position"
        )


@register_list_view
class SponsorList(ListView):
    model = Dog
    template_name = "dogs/sponsor_list.html"

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SPONSOR).order_by("reserved", "position")


class SponsorDetail(DetailView):
    model = Dog
    template_name = "dogs/sponsor_details.html"
    lookup_field = "slug"

    def get_context_data(self, form=None, form_success=False, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context["sponsor_links"] = SponsorshipInfoLink.objects.all()
        if form is not None:
            context["form"] = form
        else:
            context["form"] = SponsorForm(initial={"dog": self.object})
        context["form_success"] = form_success

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = SponsorForm(data=request.POST, files=request.FILES)
        form_success = False

        dog = Dog.objects.get(slug=kwargs.get("slug"))
        form.dog = dog
        if form.is_valid():
            instance = form.save()
            instance.send_email()
            form_success = True

        return self.render_to_response(self.get_context_data(form=form, form_success=form_success, **kwargs))


class DogDetail(DetailView):
    model = Dog
    template_name = "dogs/details.html"
    lookup_field = "slug"

    def get_object(self):
        try:
            return super().get_object()
        except MultipleObjectsReturned:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            objects = self.get_queryset().filter(**lookup)
            Dog._meta.get_field("slug").overwrite = True
            for obj in objects[1:]:
                obj.save()

            return objects[0]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if self.object.dogStatus == Dog.STATUS_LOOKING:
            return self.render_to_response(context)

        context["dog_list"] = Dog.objects.filter(dogStatus=Dog.STATUS_LOOKING).order_by("reserved", "position")[:4]
        self.template_name = "dogs/410.html"

        response = self.render_to_response(context)
        response.status_code = 410

        return response


class SuccessDogDetail(DetailView):
    model = Dog
    template_name = "dogs/success_details.html"
    lookup_field = "slug"

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SUCCESS)


@register_list_view
class SuccessList(ListView):
    model = Dog
    template_name = "dogs/success_list.html"

    def get_queryset(self):
        return self.model._default_manager.filter(dogStatus=Dog.STATUS_SUCCESS)
