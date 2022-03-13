# Django
from django.urls import path

# First Party
from team import views

app_name = "team"
urlpatterns = [
    path("", views.TeamList.as_view(), name="TeamList"),
]
