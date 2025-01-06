from django.shortcuts import render
from .utils import text_to_html_spans, verse

# Unpack all three return values
verse_html, tokens_count, total_diacritics = text_to_html_spans(verse)

def index(request):
    return render(
        request,
        "diacriticizer/index.html",
        {
            "verse": verse_html, 
            "tokens_count": tokens_count,
            "total_diacritics": total_diacritics  # Add this to context
        },
    )