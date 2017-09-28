from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^(?P<term>[\w-]+)/$', views.results, name='searchResults'),
]
