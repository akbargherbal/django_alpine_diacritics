from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseServerError
from .utils import text_to_html_spans
import logging

logger = logging.getLogger(__name__)

# Define verses list
VERSES = [
    """الَّذِينَ يَنقُضُونَ عَهْدَ اللَّهِ مِن بَعْدِ مِيثَاقِهِ وَيَقْطَعُونَ مَا أَمَرَ اللَّهُ بِهِ أَن يُوصَلَ""",
    """وَإِذَا قِيلَ لَهُمْ لَا تُفْسِدُوا فِي الْأَرْضِ قَالُوا إِنَّمَا نَحْنُ مُصْلِحُونَ""",
]


def home(request):
    return render(request, "diacriticizer/home.html")


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


def get_next_verse(request):
    """Handle HTMX request for next verse."""
    try:
        # Get current verse index from session
        current_idx = request.session.get("verse_index", 0)
        logger.debug(f"Current verse index: {current_idx}")

        # Calculate next verse index
        next_idx = (current_idx + 1) % len(VERSES)
        request.session["verse_index"] = next_idx
        logger.debug(f"Next verse index: {next_idx}")

        # Get current mode
        mode = request.GET.get("mode", "dicr")
        logger.debug(f"Mode: {mode}")

        # Get the verse text
        verse_text = VERSES[next_idx]
        logger.debug(f"Processing verse: {verse_text[:50]}...")  # Log first 50 chars

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
            # Try rendering the partial template
            response_html = render_to_string(
                "diacriticizer/partials/text_content.html",
                context,
                request=request,  # Add request to context
            )
            return HttpResponse(response_html)
        except Exception as template_error:
            logger.error(f"Template rendering error: {str(template_error)}")
            return HttpResponseServerError(f"Template error: {str(template_error)}")

    except Exception as e:
        logger.error(f"Error in get_next_verse view: {str(e)}")
        return HttpResponseServerError(f"Error processing next verse: {str(e)}")


def training(request):
    """Redirect to index page with train mode."""
    return redirect("/index/?mode=train")
