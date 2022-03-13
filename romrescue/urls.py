# Django
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

# First Party
from romrescue.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("dogs/", include("dogs.urls", namespace="dogs")),
    path("team/", include("team.urls", namespace="team")),
    path("testimonial/", include("testimonials.urls", namespace="testimonial")),
    path("donate/", include("donate.urls", namespace="donate")),
    path("", include("pages.urls", namespace="pages")),
    re_path(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

handler404 = "pages.views.error404"

if settings.DEBUG:
    # Third Party
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls, namespace="debugtoolbar")),)
    urlpatterns += (
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),
    )
