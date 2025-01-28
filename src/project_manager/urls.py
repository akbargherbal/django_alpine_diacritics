from django.urls import path
from . import views

app_name = "project_manager"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="project_list"),
    path("create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path(
        "document/<int:pk>/", views.DocumentDetailView.as_view(), name="document_detail"
    ),
    path("verse/<int:pk>/", views.VerseDetailView.as_view(), name="verse_detail"),
    path(
        "verse/<int:pk>/status/",
        views.VerseStatusUpdateView.as_view(),
        name="verse_status_update",
    ),
]
