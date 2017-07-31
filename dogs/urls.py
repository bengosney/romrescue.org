from django.conf.urls import url

from . import views

app_name = 'dogs'
urlpatterns = [
    url(r'^success/(?P<slug>[\w-]+)/$',
        views.SuccessDogDetail.as_view(),
        name='SuccessDetail'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.DogDetail.as_view(),
        name='DogDetails'),
]
