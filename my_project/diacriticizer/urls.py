from django.urls import path
from . import views

app_name = "diacriticizer"


urlpatterns = [
    path("", views.home, name="home"),
    path("training/", views.training, name="training"),
    path("index/", views.index, name="index"),
]
