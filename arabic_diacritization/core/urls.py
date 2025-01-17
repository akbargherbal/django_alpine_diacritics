from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),  # Root URL patterns
    path("diacriticizer/", include("diacriticizer.urls")),
    path("projects/", include("project_manager.urls")),
]
