# Django
from django.urls import path

# First Party
from testimonials import views

app_name = "testimonials"
urlpatterns = [
    path("", views.TestimonialList.as_view(), name="TestimonialList"),
]
