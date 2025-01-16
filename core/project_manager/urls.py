# project_manager/urls.py
from django.urls import path
from . import views

app_name = "project_manager"

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("create/", views.project_create, name="project_create"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path("document/<int:pk>/", views.document_detail, name="document_detail"),
    path("document/<int:doc_pk>/verses/", views.verse_list, name="verse_list"),
    path("verse/<int:pk>/", views.verse_detail, name="verse_detail"),
    path(
        "verse/<int:pk>/status/", views.update_verse_status, name="update_verse_status"
    ),
]
