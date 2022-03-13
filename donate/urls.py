# Django
from django.urls import path

# First Party
from donate import views

app_name = "donate"
urlpatterns = [
    path("", views.donate, name="donateform"),
]
