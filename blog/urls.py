from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$',views.BlogList.as_view(), name='BlogList'),
    url(r'^(?P<slug>[\w-]+)/$', views.BlogDetail.as_view(),name='BlogDetail'),
]
