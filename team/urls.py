# Django
from django.conf.urls import url

# Locals
from . import views

app_name = 'team'
urlpatterns = [
    url(r'^$', views.TeamList.as_view(), name='TeamList'),
]
