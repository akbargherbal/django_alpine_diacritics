from django.shortcuts import render

from django.views.generic import TemplateView
from project_manager.models import Project


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_projects"] = Project.objects.filter(is_active=True).count()
        return context


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class GuidePageView(TemplateView):
    template_name = "pages/guide.html"
