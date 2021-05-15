# Django
from django.conf.urls import url

# First Party
from donate import views

app_name = "donate"
urlpatterns = [
    url("", views.donate, name="donateform"),
]
