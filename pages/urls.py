# Django
from django.urls import path, re_path

# First Party
from pages import views

app_name = "pages"
urlpatterns = [
    path("intrest/", views.IntrestView.as_view(), name="intrest"),
    re_path(r"^intrest/(?P<slug>[\w-]+)/$", views.IntrestSuccessView.as_view(), name="intrest_success"),
    re_path(r"^(?P<slug>[\w-]+)/$", views.PageView.as_view(), name="page"),
    re_path(r"^(?P<slug>[\w-]+)/success$", views.PageView.as_view(), {"success": True}, name="page_success"),
    re_path(r"^(?P<slug>[\w-]+)/list$", views.ModuleListView.as_view(), name="modulelist"),
    path("", views.HomePage.as_view(), name="home"),
]
