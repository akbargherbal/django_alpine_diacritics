from django.contrib import admin
from .models import Project


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "project_type", "created_at", "is_active"]
    list_filter = ["project_type", "is_active"]
    search_fields = ["name"]
    ordering = ["-created_at"]
