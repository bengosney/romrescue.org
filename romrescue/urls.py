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
    url(r"^donate/", include("donate.urls", namespace="donate")),
    url(r"^", include("pages.urls", namespace="pages")),
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

handler404 = "pages.views.error404"

if settings.DEBUG:
    # Third Party
    import debug_toolbar

    urlpatterns += (url(r"^__debug__/", include(debug_toolbar.urls, namespace="debugtoolbar")),)
    urlpatterns += (url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True}),)
