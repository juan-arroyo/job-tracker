from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # delegate all tracker URLs to the tracker app
    path("", include("tracker.urls", namespace="tracker")),
]