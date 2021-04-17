# Django
from django.conf.urls import url

# First Party
from testimonials import views

app_name = "testimonials"
urlpatterns = [
    url(r"^$", views.TestimonialList.as_view(), name="TestimonialList"),
]
