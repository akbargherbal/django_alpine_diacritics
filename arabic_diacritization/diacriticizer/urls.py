from django.urls import path
from . import views

app_name = "diacriticizer"


urlpatterns = [
    path(
        "", views.home, name="home"
    ),  # this makes the homepage reachable by `/` route.
    path("training/", views.training, name="training"),
    path("index/", views.index, name="index"),
    path("next-sentence/", views.get_next_verse, name="next-sentence"),
]
