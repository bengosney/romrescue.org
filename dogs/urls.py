from django.conf.urls import url

from . import views

app_name = 'dogs'
urlpatterns = [
    url(r'^$', views.AdoptionList.as_view(), name='AdoptionList'),
    url(r'^success/(?P<slug>[\w-]+)/$', views.SuccessDogDetail.as_view(), name='SuccessDetail'),
    url(r'^success/$', views.SuccessList.as_view(), name='SuccessList'),
    url(r'^(?P<slug>[\w-]+)/$', views.DogDetail.as_view(), name='DogDetails'),
]
