from django.conf.urls import url

from . import views

app_name = 'photocomp'
urlpatterns = [
    url(r'^$',
        views.CompitionList.as_view(),
        name='CompitionList'),
    url(r'^(?P<slug>[\w-]+)/$',
        views.CompitionDetail.as_view(),
        name='CompitionDetails'),
    url(r'^(?P<comp_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        views.CategoryDetails.as_view(),
        name='CategoryDetails'),
    url(r'^(?P<comp_slug>[\w-]+)/(?P<slug>[\w-]+)/submission/$',
        views.CategorySubmission.as_view(),
        name='CategorySubmission'),
]
