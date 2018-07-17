from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'looking', views.DogViewSet)

app_name = 'dogs'
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^success/(?P<slug>[\w-]+)/$',
        views.SuccessDogDetail.as_view(),
        name='SuccessDetail'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.DogDetail.as_view(),
        name='DogDetails'),
]
