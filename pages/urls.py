
from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', views.PageView.as_view(), name='page'),
    url(r'^(?P<slug>[\w-]+)/success$', views.PageView.as_view(), {'success': True}, name='page_success'),
    url(r'^(?P<slug>[\w-]+)/list$', views.ModuleListView.as_view(), name='modulelist'),
    url(r'^$', views.HomePage.as_view(), name='home'),
]
