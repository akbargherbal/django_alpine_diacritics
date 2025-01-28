# project_manager/utils.py
from typing import List, Dict
from io import TextIOWrapper

from django.core.files.uploadedfile import UploadedFile
import regex as re
from project_manager.ar_data import set_ar_dia, list_ar_alpha
from project_manager.models import Document, Verse


def process_uploaded_file(document: Document) -> List[Dict]:
    """Process the uploaded file and split it into verses."""
    verses = []
    try:
        with document.file.open("rb") as file:
            text_file = TextIOWrapper(file, encoding="utf-8")
            content = text_file.read()

        # Split into verses (by lines, removing empty ones)
        lines = [line.strip() for line in content.split("\n") if line.strip()]

        # Create verse data
        for position, line in enumerate(lines, 1):
            verses.append({"content": line, "position": position, "document": document})

    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")

    return verses


def create_verses_from_data(verses_data: List[Dict]) -> List[Verse]:
    """Create Verse objects from processed data."""
    return [Verse.objects.create(**verse_data) for verse_data in verses_data]


def get_file_size_kb(file: UploadedFile) -> int:
    """Get file size in KB."""
    return file.size // 1024


def split_arabic_text(word: str, set_ar_dia: set = set_ar_dia) -> list[tuple[str, str]]:
    """Split Arabic word into (character, diacritics) tuples."""
    pattern_dia = f'[{"".join(set_ar_dia)}]*'
    pattern_non_dia = f'[^{"".join(set_ar_dia)}]'
    pattern = f"{pattern_non_dia}{pattern_dia}"
    matches = re.findall(pattern, word)
    return [(item[0], item[1:]) if len(item) > 1 else (item[0], "") for item in matches]


def create_char_span(char: str, char_idx: int, global_dia_idx: int) -> str:
    """Create HTML span for a character."""
    return (
        f'<span data-char-idx="{char_idx}" '
        f'data-global-char-idx="{global_dia_idx}" '
        f'class="char">{char}</span>'
    )


def create_dia_span(diacritics: str, char_idx: int, global_dia_idx: int) -> str:
    """Create HTML span for diacritics."""
    return (
        f'<span data-dia-idx="{char_idx}" '
        f'data-global-dia-idx="{global_dia_idx}" '
        f'data-dia="{diacritics}" '
        f'class="char"></span>'
    )


def create_word_span(html_chars: list[str], wd_idx: int) -> str:
    """Create HTML span for a word."""
    return f'<span data-wd-idx="{wd_idx}" ' f'class="word">{"".join(html_chars)}</span>'


def char_has_dia(char, dia, mode):
    if mode == "train" and char in list_ar_alpha and dia:
        return True
    elif mode == "dicr" and char in list_ar_alpha:
        return True
    else:
        return False


def text_to_html_spans(text, mode="dicr"):
    if mode not in ["dicr", "train"]:
        raise ValueError("Mode must be either 'dicr' or 'train'")

    list_words = text.split()
    tokens_count = len(list_words)
    html_content = []
    global_dia_idx = 0
    wd_dict = {}
    char_dict_global = {}
    char_dict_local = {}

    for wd_idx, word in enumerate(list_words):
        list_chars_span = split_arabic_text(word)

        # This is the only difference between train and dic modes
        if mode == "train":
            wd_dia_count = len([i for i in list_chars_span if i[1]])
        else:  # dicr mode
            wd_dia_count = len([i for i in list_chars_span if i[0] in list_ar_alpha])

        html_chars = []
        is_word = wd_dia_count > 0

        wd_dict[wd_idx] = {"isWord": is_word, "wordDiaCount": wd_dia_count}

        char_idx = 0
        for char, diacritics in list_chars_span:
            char_is_alpha = char in list_ar_alpha
            has_dia = char_has_dia(char, diacritics, mode)

            if char_is_alpha and has_dia:
                char_span = create_char_span(char, char_idx, global_dia_idx)
                dia_span = create_dia_span(diacritics, char_idx, global_dia_idx)

                char_data = {
                    "char": char,
                    "dia": diacritics,
                    "in_word": is_word,
                    "has_dia": True,
                    "wd_idx": wd_idx,
                    "local_char_idx": char_idx,
                    "global_dia_idx": global_dia_idx,
                }

                char_dict_global[global_dia_idx] = char_data
                char_dict_local[f"{wd_idx}_{char_idx}"] = char_data

                html_chars.append(char_span + dia_span)
                char_idx += 1
                global_dia_idx += 1
            else:
                html_chars.append(f'<span class="char">{char}</span>')

        word_span = create_word_span(html_chars, wd_idx)
        html_content.append(word_span)
        total_diacritics = global_dia_idx

    return (
        " ".join(html_content),
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    )
