from django.conf.urls import url

from . import views

app_name = 'ajax'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.ajax_view.as_view(), name='call'),
]
