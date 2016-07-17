from django.conf.urls import url

from . import views

app_name = 'dogs'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.DogDetail.as_view(), name='DogDetails'),
    url(r'^$', views.AdoptionList.as_view(), name='AdoptionList'),
]
