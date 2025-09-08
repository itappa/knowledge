from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("accounts/", include("allauth.urls")),
        path("inquiry/", include("inquiry.urls")),
        path("knowledge/", include("knowledge.urls")),
        path("", include("common.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
