# Third Party
from vanilla import ListView

# First Party
from pages.decorators import register_list_view
from testimonials.models import Testimonial


@register_list_view
class TestimonialList(ListView):
    model = Testimonial
    template_name = "testimonials/list.html"
