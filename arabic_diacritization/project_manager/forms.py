from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder
from .models import Project, Document
from .utils import get_file_size_kb


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("name", css_class="form-input"),
            Field("project_type", css_class="form-select"),
            ButtonHolder(
                Submit("submit", "Create Project", css_class="pm-btn pm-btn-primary")
            ),
        )

    class Meta:
        model = Project
        fields = ["name", "project_type"]
        help_texts = {
            "name": "Choose a descriptive name for your project",
            "project_type": "Select whether this is a training or diacritization project",
        }


class DocumentUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_enctype = "multipart/form-data"
        self.helper.layout = Layout(
            Field("name", css_class="form-input"),
            Field("file"),
            ButtonHolder(
                Submit("submit", "Upload Document", css_class="pm-btn pm-btn-primary")
            ),
        )

    class Meta:
        model = Document
        fields = ["name", "file"]

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
