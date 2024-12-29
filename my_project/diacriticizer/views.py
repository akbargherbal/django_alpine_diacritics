from django.shortcuts import render

# Create your views here.
from .utils import text_to_html_spans, verse

verse_html, tokens_count = text_to_html_spans(verse)


def index(request):
    return render(
        request,
        "diacriticizer/index.html",
        {"verse": verse_html, "tokens_count": tokens_count},
    )
