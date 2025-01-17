from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.messages.views import SuccessMessageMixin

from .models import Project, Document, Verse
from .forms import ProjectForm, DocumentUploadForm
from .utils import process_uploaded_file, create_verses_from_data


class ProjectListView(ListView):
    model = Project
    template_name = "project_manager/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(is_active=True)


class ProjectCreateView(SuccessMessageMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "project_manager/project_form.html"
    success_message = "Project created successfully."

    def get_success_url(self):
        return reverse_lazy(
            "project_manager:project_detail", kwargs={"pk": self.object.pk}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Project"
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "project_manager/project_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["documents"] = self.object.documents.all()
        context["form"] = DocumentUploadForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.project = self.object
            document.file_size = form.cleaned_data["file"].size // 1024
            document.save()

            try:
                verses_data = process_uploaded_file(document)
                create_verses_from_data(verses_data)
                messages.success(
                    request, "Document uploaded and processed successfully."
                )
                return redirect("project_manager:project_detail", pk=self.object.pk)
            except Exception as e:
                document.delete()
                messages.error(request, str(e))
                return self.render_to_response(self.get_context_data(form=form))

        return self.render_to_response(self.get_context_data(form=form))


class DocumentDetailView(DetailView):
    model = Document
    template_name = "project_manager/document_detail.html"
    context_object_name = "document"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["verses"] = self.object.verses.all()
        return context


class VerseDetailView(DetailView):
    model = Verse
    template_name = "project_manager/verse_detail.html"
    context_object_name = "verse"


class VerseStatusUpdateView(View):
    def post(self, request, pk):
        verse = get_object_or_404(Verse, pk=pk)
        new_status = request.POST.get("status")

        if new_status in dict(Verse.Status.choices):
            verse.status = new_status
            verse.save()
            return HttpResponse(verse.get_status_display())

        return HttpResponseBadRequest("Invalid status")
