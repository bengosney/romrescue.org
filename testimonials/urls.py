# Django
from django.conf.urls import url

# Locals
from . import views

app_name = 'testimonials'
urlpatterns = [
    url(r'^$', views.TestimonialList.as_view(), name='TestimonialList'),
]
