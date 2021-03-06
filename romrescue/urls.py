"""romrescue URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Django
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

# First Party
from romrescue.sitemaps import sitemaps

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^ckeditor/", include("ckeditor_uploader.urls")),
    url(r"^dogs/", include("dogs.urls", namespace="dogs")),
    url(r"^team/", include("team.urls", namespace="team")),
    url(r"^testimonial/", include("testimonials.urls", namespace="testimonial")),
    url(r"^", include("pages.urls", namespace="pages")),
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

handler404 = "pages.views.error404"

if settings.DEBUG:
    # Third Party
    import debug_toolbar

    urlpatterns += (url(r"^__debug__/", include(debug_toolbar.urls, namespace="debugtoolbar")),)
    urlpatterns += (url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),)
