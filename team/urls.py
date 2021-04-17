# Django
from django.conf.urls import url

# First Party
from team import views

app_name = "team"
urlpatterns = [
    url(r"^$", views.TeamList.as_view(), name="TeamList"),
]
