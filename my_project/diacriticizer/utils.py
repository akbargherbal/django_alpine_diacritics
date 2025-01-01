ar_alpha =['ء',
 'آ',
 'أ',
 'ؤ',
 'إ',
 'ئ',
 'ا',
 'ب',
 'ة',
 'ت',
 'ث',
 'ج',
 'ح',
 'خ',
 'د',
 'ذ',
 'ر',
 'ز',
 'س',
 'ش',
 'ص',
 'ض',
 'ط',
 'ظ',
 'ع',
 'غ',
 'ف',
 'ق',
 'ك',
 'ل',
 'م',
 'ن',
 'ه',
 'و',
 'ى',
 'ي']

verse = '''
إن الذي ســـمـــك السماء، بنى لنا ... بيتا: دعائمه أعز وأطول
'''.strip()


def text_to_html_spans(text: str) -> str:
   """Convert text to HTML with word and character spans."""
   list_words = text.split()
   tokens_count = len(list_words)
   html_content = []

#    char_counter = 0
   list_words =  [(idx, word) for (idx, word) in enumerate(list_words)]

   for (wd_idx, word) in list_words:
       html_chars = []
       word_len = len([i for i in word if i in ar_alpha])
       is_word = "true"
       is_word = "false" if word_len == 0 else is_word
       char_idx = -1
       for char in word:
           char_is_alpha = char in ar_alpha
           char_idx = char_idx + 1 if char_is_alpha else char_idx
           idx_attr = f'data-char-idx="{char_idx}"' if char_is_alpha else ''
           idx_attr_dia = f'data-dia-idx={char_idx}' if char_is_alpha else ''
           
           html_chars.append(f'<span {idx_attr}class="char">{char}</span><span {idx_attr_dia} class="dia"></span>')

           
       html_word = f'<span class="word" data-is-word="{is_word}" data-wd-idx="{wd_idx}" data-wd-len="{word_len}">{"".join(html_chars)}</span>'
       html_content.append(html_word)
   html_content = " ".join(html_content)
   return html_content, tokens_count

