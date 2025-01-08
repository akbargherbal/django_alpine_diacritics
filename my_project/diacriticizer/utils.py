import regex as re
from collections import defaultdict
from .ar_data import set_ar_dia, list_ar_alpha

verse = """
الَّذِينَ يَنقُضُونَ (عَهْدَ) اللَّهِ مِن بَعْدِ مِيثَاقِهِ وَيَقْطَعُونَ مَا أَمَرَ اللَّهُ بِهِ  notowrd أَن يُوصَلَ وَيُفْسِدُونَ فِي الْأَرْضِ ۚ أُولَـٰئِكَ هُمُ الْخَاسِرُونَ
""".strip()


def split_arabic_text(word, set_ar_dia=set_ar_dia):
    """
    Split Arabic word into a list of tuples containing (character, diacritics).

    Args:
        word (str): Arabic word with or without diacritics

    Returns:
        list: List of tuples where each tuple contains (character, diacritics)
    """
    pattern_dia = f'[{"".join(set_ar_dia)}]*'
    pattern_non_dia = (
        f'[^{"".join(set_ar_dia)}]'  # Any character that's not a diacritic
    )
    pattern = f"{pattern_non_dia}{pattern_dia}"

    matches = re.findall(pattern, word)
    return [(item[0], item[1:]) if len(item) > 1 else (item[0], "") for item in matches]


def text_to_html_spans(text: str) -> tuple[str, int, int]:
    """
    Convert text to HTML with word and character spans.
    Returns: (html_content, tokens_count, total_diacritics)
    """
    list_words = text.split()
    tokens_count = len(list_words)
    html_content = []
    global_dia_idx = 0
    wd_dict = {}
    char_dict_global = defaultdict(dict)
    char_dict_local = defaultdict(dict)

    for wd_idx, word in enumerate(list_words):
        # Split word into characters and their diacritics
        list_chars_span = split_arabic_text(word)
        wd_dia_count = len([i for i in list_chars_span if i[1]])

        html_chars = []
        is_word = wd_dia_count > 0

        if is_word:
            wd_dict[wd_idx] = {"isWord": True, "wordDiaCount": wd_dia_count}
        else:
            wd_dict[wd_idx] = {"isWord": False, "wordDiaCount": 0}

        char_idx = 0
        for char, diacritics in list_chars_span:
            char_is_alpha = char in list_ar_alpha
            char_has_dia = diacritics != ""

            if char_is_alpha and char_has_dia:
                # Handle Arabic chars with diacritics - needs indexing
                char_span = (
                    f'<span data-char-idx="{char_idx}" '
                    f'data-global-char-idx="{global_dia_idx}" '
                    f'class="char">{char}</span>'
                )

                dia_span = (
                    f'<span data-dia-idx="{char_idx}" '
                    f'data-global-dia-idx="{global_dia_idx}" '
                    f'data-dia="{diacritics}" '
                    f'class="char"></span>'
                )

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
                local_key = f"{wd_idx}_{char_idx}"
                char_dict_local[local_key] = char_data

                html_chars.append(char_span + dia_span)
                char_idx += 1
                global_dia_idx += 1

            else:
                # Handle both Arabic chars without diacritics and non-Arabic characters
                html_chars.append(f'<span class="char">{char}</span>')

        # Combine into word span
        word_span = (
            f'<span data-wd-idx="{wd_idx}" '
            f'class="word">{"".join(html_chars)}</span>'
        )
        html_content.append(word_span)

    total_diacritics = global_dia_idx
    char_dict_global = dict(char_dict_global)
    char_dict_local = dict(char_dict_local)

    html_content = " ".join(html_content)
    return (
        html_content,
        tokens_count,
        total_diacritics,
        wd_dict,
        char_dict_global,
        char_dict_local,
    )
