import os
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls import re_path
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

if os.environ.get("IS_DOCKER", None) is not None:
    urlpatterns += [
        re_path(
            r"^uploads/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]

    urlpatterns += [
        re_path(
            r"^public/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.STATIC_ROOT,
            },
        ),
    ]

urlpatterns += [path("", include(wagtail_urls))]
