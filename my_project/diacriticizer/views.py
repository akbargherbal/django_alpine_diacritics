from django.shortcuts import render, redirect
from .utils import text_to_html_spans, verse


def home(request):
    return render(request, "diacriticizer/home.html")


def index(request):
    """
    Render the main diacriticizer page with processed verse data.
    """
    # Determine the mode based on GET parameter; default to 'dicr'
    mode = request.GET.get("mode", "dicr")

    # Generate processed data based on the mode
    (
        verse_html,
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    ) = text_to_html_spans(verse, mode=mode)

    # Prepare context for rendering
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


def training(request):
    """
    Redirect to the index page with mode set to 'train'.
    """
    return redirect("/index/?mode=train")  # Use the actual URL path
