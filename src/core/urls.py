from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("frontend.urls",namespace="frontend")),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Serve static files with cache control headers
    path(
        f"{settings.STATIC_URL}<path:path>",
        serve,
        {"document_root": settings.STATIC_ROOT, "show_indexes": True, "cache_timeout": settings.CACHE_MIDDLEWARE_SECONDS},
    ),

]

admin.site.site_header = 'Makalu ADministrator'



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


