from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseServerError
from .utils import text_to_html_spans
import logging
from django.http import HttpResponse

from project_manager.models import Document

logger = logging.getLogger(__name__)

# Define verses list
VERSES = [
    """الَّذِينَ يَنقُضُونَ عَهْدَ اللَّهِ مِن بَعْدِ مِيثَاقِهِ وَيَقْطَعُونَ مَا أَمَرَ اللَّهُ بِهِ أَن يُوصَلَ""",
    """وَإِذَا قِيلَ لَهُمْ لَا تُفْسِدُوا فِي الْأَرْضِ قَالُوا إِنَّمَا نَحْنُ مُصْلِحُونَ""",
]


# Using more descriptive name (recommended)
def get_document_verses(project_id, document_id):
    """
    Get verses for a specific document within a project context.

    Args:
        project_id: The ID of the project
        document_id: The ID of the document

    Returns:
        QuerySet of verses ordered by position or None if document not found
    """
    try:
        document = Document.objects.get(project_id=project_id, id=document_id)
        return document.verses.all().order_by("position")
    except Document.DoesNotExist:
        return None


def index(request):
    """Render the main diacriticizer page with processed verse data."""
    mode = request.GET.get("mode", "dicr")

    try:
        # Process initial verse (first verse)
        (
            verse_html,
            tokens_count,
            total_diacritics,
            wd_dict,
            char_dict_global,
            char_dict_local,
        ) = text_to_html_spans(VERSES[0], mode=mode)

        # Initialize session with first verse
        request.session["verse_index"] = 0

        context = {
            "verse": verse_html,
            "tokens_count": tokens_count,
            "total_diacritics": total_diacritics,
            "wd_dict": wd_dict,
            "char_dict_global": char_dict_global,
            "char_dict_local": char_dict_local,
            "mode": mode,
        }

        return render(request, "diacriticizer/index.html", context)

    except Exception as e:
        print(f"Error in index view: {str(e)}")
        return HttpResponseServerError("Error processing verse")


def training(request):
    """Redirect to index page with train mode."""
    return redirect("/diacriticizer/?mode=train")


def get_next_verse(request):
    """Handle HTMX request for next verse from the current document."""
    try:
        # Get document info from session
        verse_ids = request.session.get("document_verses_ids", [])
        current_idx = request.session.get("verse_index", 0)
        doc_info = request.session.get("current_document", {})

        if not verse_ids:
            return HttpResponseServerError("No verses found in session")

        # Calculate next verse index
        next_idx = (current_idx + 1) % len(verse_ids)
        request.session["verse_index"] = next_idx

        # Get mode from session or default to diacritization
        mode = doc_info.get("project_type", "dicr")

        # Get the verse from database
        from project_manager.models import Verse

        try:
            verse = Verse.objects.get(id=verse_ids[next_idx])
            verse_text = verse.content
        except Verse.DoesNotExist:
            return HttpResponseServerError("Verse not found")

        # Process next verse
        (
            verse_html,
            tokens_count,
            total_diacritics,
            wd_dict,
            char_dict_global,
            char_dict_local,
        ) = text_to_html_spans(verse_text, mode=mode)

        context = {
            "verse": verse_html,
            "tokens_count": tokens_count,
            "total_diacritics": total_diacritics,
            "wd_dict": wd_dict,
            "char_dict_global": char_dict_global,
            "char_dict_local": char_dict_local,
            "mode": mode,
        }

        try:
            response_html = render_to_string(
                "diacriticizer/partials/text_content.html",
                context,
                request=request,
            )
            return HttpResponse(response_html)
        except Exception as template_error:
            logger.error(f"Template rendering error: {str(template_error)}")
            return HttpResponseServerError(f"Template error: {str(template_error)}")

    except Exception as e:
        logger.error(f"Error in get_next_verse view: {str(e)}")
        return HttpResponseServerError(f"Error processing next verse: {str(e)}")


def process_document(request):
    """
    Process a specific document's verses for diacritization or training.
    """
    # Get parameters from URL
    project_id = request.GET.get("project_id")
    doc_id = request.GET.get("doc_id")
    project_type = request.GET.get(
        "project_type", "dicr"
    )  # Default to diacritization mode
    doc_name = request.GET.get("doc_name", "")

    try:
        # Get verses from the document
        verses = get_document_verses(project_id, doc_id)
        if not verses:
            return HttpResponseServerError("Document not found or has no verses")

        # Process initial verse (first verse)
        first_verse = verses.first()
        if not first_verse:
            return HttpResponseServerError("No verses found in document")

        (
            verse_html,
            tokens_count,
            total_diacritics,
            wd_dict,
            char_dict_global,
            char_dict_local,
        ) = text_to_html_spans(first_verse.content, mode=project_type)

        # Store verses QuerySet in session
        request.session["document_verses_ids"] = list(
            verses.values_list("id", flat=True)
        )
        request.session["verse_index"] = 0
        request.session["current_document"] = {
            "project_id": project_id,
            "doc_id": doc_id,
            "project_type": project_type,
            "doc_name": doc_name,
        }

        context = {
            "verse": verse_html,
            "tokens_count": tokens_count,
            "total_diacritics": total_diacritics,
            "wd_dict": wd_dict,
            "char_dict_global": char_dict_global,
            "char_dict_local": char_dict_local,
            "mode": project_type,
            "document_name": doc_name,
        }

        return render(request, "diacriticizer/index.html", context)

    except Exception as e:
        logger.error(f"Error in process_document view: {str(e)}")
        return HttpResponseServerError(f"Error processing document: {str(e)}")
