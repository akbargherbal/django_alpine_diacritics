from django.urls import path
from . import views

app_name = "diacriticizer"

urlpatterns = [
    path("", views.index, name="index"),  # Main diacritization interface
    path("training/", views.training, name="training"),  # Training mode
    path("next-sentence/", views.get_next_verse, name="next-sentence"),  # HTMX endpoint
    path("process/", views.process_document, name="process"),
]
