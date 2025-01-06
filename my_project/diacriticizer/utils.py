ar_alpha = [
    'ء', 'آ', 'أ', 'ؤ', 'إ', 'ئ', 'ا', 'ب', 'ة', 'ت', 'ث', 'ج', 'ح', 'خ',
    'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق',
    'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ى', 'ي'
]

verse = '''
إن الذي ســـمـــك السماء، (بنى) لنا ... بيتا: دعائمه أعز وأطول
'''.strip()

def text_to_html_spans(text: str) -> tuple[str, int, int]:
    """
    Convert text to HTML with word and character spans.
    Returns: (html_content, tokens_count, total_diacritics)
    """
    list_words = text.split()
    tokens_count = len(list_words)
    html_content = []
    global_dia_idx = 0  # Initialize global diacritic counter

    list_words = [(idx, word) for (idx, word) in enumerate(list_words)]

    for (wd_idx, word) in list_words:
        html_chars = []
        word_len = len([i for i in word if i in ar_alpha])
        is_word = "true"
        is_word = "false" if word_len == 0 else is_word
        char_idx = 0
        
        for char in word:
            char_is_alpha = char in ar_alpha
            idx_attr = f'data-char-idx="{char_idx}" data-global-char-idx="{global_dia_idx}"' if char_is_alpha else ''
            
            
            # Add global dia index only for actual characters that need diacritics
            if char_is_alpha:
                idx_attr_dia = f'data-dia-idx="{char_idx}" data-global-dia-idx="{global_dia_idx}"'
                char_idx = char_idx + 1 if char_is_alpha else char_idx
                global_dia_idx += 1  # Increment global counter
            else:
                idx_attr_dia = ''
            
            html_chars.append(f'<span {idx_attr} class="char">{char}</span><span {idx_attr_dia}></span>')

        html_word = f'<span class="word" data-is-word="{is_word}" data-wd-idx="{wd_idx}" data-wd-len="{word_len}">{"".join(html_chars)}</span>'
        html_content.append(html_word)
    
    html_content = " ".join(html_content)
    return html_content, tokens_count, global_dia_idx