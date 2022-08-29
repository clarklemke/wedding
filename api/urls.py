from rest_framework import permissions
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ping import views as ping_views
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="SSAPI",
        default_version="v1",
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r"^ping/", ping_views.Ping.as_view(), name="ping"),
    path("admin/", admin.site.urls),
    path("", include("guests.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
