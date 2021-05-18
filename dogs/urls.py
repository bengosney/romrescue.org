# Django
from django.conf.urls import include, url

# Third Party
from rest_framework import routers

# First Party
from dogs import views

router = routers.DefaultRouter()
router.register(r"looking", views.DogViewSet)

app_name = "dogs"
urlpatterns = [
    # url(r"^api/", include((router.urls, "app"), namespace="api")),
    url(r"^success/(?P<slug>[\w-]+)/$", views.SuccessDogDetail.as_view(), name="SuccessDetail"),
    url(r"^sponsor/(?P<slug>[\w-]+)/$", views.SponsorDetail.as_view(), name="SponsorDetail"),
    url(r"^(?P<slug>[\w-]+)/$", views.DogDetail.as_view(), name="DogDetails"),
]
