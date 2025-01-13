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


def get_char_data(
    char: str,
    diacritics: str,
    is_word: bool,
    wd_idx: int,
    char_idx: int,
    global_dia_idx: int,
) -> dict:
    """Create metadata for a character."""
    return {
        "char": char,
        "dia": diacritics,
        "in_word": is_word,
        "has_dia": bool(diacritics),
        "wd_idx": wd_idx,
        "local_char_idx": char_idx,
        "global_dia_idx": global_dia_idx,
    }


def text_to_spans_train(text: str) -> tuple[str, int, int, dict, dict, dict]:
    """Convert text to HTML spans for training, preserving original diacritics."""
    list_words = text.split()
    tokens_count = len(list_words)
    html_content = []
    global_dia_idx = 0
    wd_dict = {}
    char_dict_global = {}
    char_dict_local = {}

    for wd_idx, word in enumerate(list_words):
        list_chars_span = split_arabic_text(word)
        wd_dia_count = len([i for i in list_chars_span if i[1]])

        html_chars = []
        is_word = wd_dia_count > 0

        wd_dict[wd_idx] = {"isWord": is_word, "wordDiaCount": wd_dia_count}

        char_idx = 0
        for char, diacritics in list_chars_span:
            char_is_alpha = char in list_ar_alpha
            char_has_dia = bool(diacritics)

            if char_is_alpha and char_has_dia:
                char_span = create_char_span(char, char_idx, global_dia_idx)
                dia_span = create_dia_span(diacritics, char_idx, global_dia_idx)

                char_data = get_char_data(
                    char, diacritics, is_word, wd_idx, char_idx, global_dia_idx
                )

                char_dict_global[global_dia_idx] = char_data
                char_dict_local[f"{wd_idx}_{char_idx}"] = char_data

                html_chars.append(char_span + dia_span)
                char_idx += 1
                global_dia_idx += 1
            else:
                html_chars.append(f'<span class="char">{char}</span>')

        word_span = create_word_span(html_chars, wd_idx)
        html_content.append(word_span)

    return (
        " ".join(html_content),
        tokens_count,
        global_dia_idx,
        wd_dict,
        char_dict_global,
        char_dict_local,
    )
