# Django
from django.conf.urls import url

# First Party
from pages import views

app_name = "pages"
urlpatterns = [
    url(r"^intrest/$", views.IntrestView.as_view(), name="intrest"),
    url(r"^intrest/(?P<slug>[\w-]+)/$", views.IntrestSuccessView.as_view(), name="intrest_success"),
    url(r"^(?P<slug>[\w-]+)/$", views.PageView.as_view(), name="page"),
    url(r"^(?P<slug>[\w-]+)/success$", views.PageView.as_view(), {"success": True}, name="page_success"),
    url(r"^(?P<slug>[\w-]+)/list$", views.ModuleListView.as_view(), name="modulelist"),
    url(r"^$", views.HomePage.as_view(), name="home"),
]
