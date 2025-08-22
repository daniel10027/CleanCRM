from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Schema & Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Apps
    path("api/accounts/", include("accounts.interfaces.routers")),
    path("api/directory/", include("directory.interfaces.routers")),
    path("api/contacts/", include("contacts.interfaces.routers")),
    path("api/campaigns/", include("campaigns.interfaces.routers")),
]