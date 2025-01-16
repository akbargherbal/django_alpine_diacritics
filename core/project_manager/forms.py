# project_manager/forms.py
from django import forms
from .models import Project, Document
from .utils import get_file_size_kb


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "project_type"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter project name",
                }
            ),
            "project_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        help_texts = {
            "name": "Choose a descriptive name for your project",
            "project_type": "Select whether this is a training or diacritization project",
        }


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""

    class Meta:
        model = Document
        fields = ["name", "file"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter document name"}
            )
        }

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file:
            # Check file size
            file_size = get_file_size_kb(file)
            if file_size > 10240:  # 10MB limit
                raise forms.ValidationError("File size must be less than 10MB.")

            # Check file extension
            if not file.name.endswith(".txt"):
                raise forms.ValidationError("Only .txt files are allowed.")

            return file
