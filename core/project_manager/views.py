# project_manager/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Project, Document, Verse
from .forms import ProjectForm, DocumentUploadForm
from .utils import process_uploaded_file, create_verses_from_data, text_to_html_spans


def project_list(request):
    """Display list of all projects."""
    projects = Project.objects.filter(is_active=True)
    return render(
        request,
        "project_manager/project_list.html",
        {"projects": projects},
    )


def project_create(request):
    """Create a new project."""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, "Project created successfully.")
            return redirect("project_manager:project_detail", pk=project.pk)
    else:
        form = ProjectForm()

    return render(
        request,
        "project_manager/project_form.html",
        {"form": form, "title": "Create Project"},
    )


def project_detail(request, pk):
    """Display project details and its documents."""
    project = get_object_or_404(Project, pk=pk)
    documents = project.documents.all()

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.project = project
            document.file_size = form.cleaned_data["file"].size // 1024
            document.save()

            try:
                # Process the uploaded file
                verses_data = process_uploaded_file(document)
                create_verses_from_data(verses_data)
                messages.success(
                    request, "Document uploaded and processed successfully."
                )
                return redirect("project_manager:project_detail", pk=pk)
            except ValidationError as e:
                document.delete()  # Cleanup if processing fails
                messages.error(request, str(e))
    else:
        form = DocumentUploadForm()

    return render(
        request,
        "project_manager/project_detail.html",
        {"project": project, "documents": documents, "form": form},
    )


def document_detail(request, pk):
    """Display document details and its verses."""
    document = get_object_or_404(Document, pk=pk)
    verses = document.verses.all()

    return render(
        request,
        "project_manager/document_detail.html",
        {"document": document, "verses": verses},
    )


def verse_list(request, doc_pk):
    """Display list of verses for a document."""
    document = get_object_or_404(Document, pk=doc_pk)
    verses = document.verses.all()

    return render(
        request,
        "project_manager/verse_list.html",
        {"document": document, "verses": verses},
    )


def verse_detail(request, pk):
    """
    Display verse detail and integrate with diacriticizer.
    """
    verse = get_object_or_404(Verse, pk=pk)
    mode = verse.document.project.project_type  # 'train' or 'dicr'

    # Process the verse content using the text_to_html_spans utility
    (
        verse_html,
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    ) = text_to_html_spans(verse.content, mode=mode)

    context = {
        "verse": verse,
        "mode": mode,
        "verse_html": verse_html,
        "tokens_count": tokens_count,
        "total_diacritics": total_diacritics,
        "wd_dict": wd_dict,
        "char_dict_global": char_dict_global,
        "char_dict_local": char_dict_local,
    }

    return render(request, "project_manager/verse_detail.html", context)


@require_http_methods(["POST"])
def update_verse_status(request, pk):
    verse = get_object_or_404(Verse, pk=pk)
    new_status = request.POST.get("status")

    if new_status in dict(Verse.Status.choices):
        verse.status = new_status
        verse.save()
        return HttpResponse(verse.get_status_display())

    return HttpResponseBadRequest("Invalid status")
