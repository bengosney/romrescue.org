# Django
from django.urls import re_path

# First Party
from dogs import views

app_name = "dogs"
urlpatterns = [
    re_path(r"^success/(?P<slug>[\w-]+)/$", views.SuccessDogDetail.as_view(), name="SuccessDetail"),
    re_path(r"^sponsor/(?P<slug>[\w-]+)/$", views.SponsorDetail.as_view(), name="SponsorDetail"),
    re_path(r"^(?P<slug>[\w-]+)/$", views.DogDetail.as_view(), name="DogDetails"),
]
