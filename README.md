I'm working on a learning project to build an Arabic text diacritization web application. As a Python developer with 5+ years of experience but limited front-end knowledge (<1 year), I'm using Django for the backend and AlpineJS for the front end. My approach prioritizes keeping JavaScript code minimal while achieving necessary real-time interactivity.

The application's core purpose is to enable fast, streamlined addition of diacritical marks (تشكيل) to Arabic text. The backend (Django) serves pre-structured HTML with comprehensive data attributes, while the front end (AlpineJS/JS) handles essential real-time interactions like keyboard navigation and diacritic insertion. The project currently uses keyboard shortcuts for efficiency (e.g., Ctrl+Space for word navigation, Space for character navigation, number keys for diacritics).

My development preferences are:

1. Keep JavaScript minimal - use frameworks/libraries (AlpineJS, hotkeys-js) to reduce custom JS code
2. Leverage Django's capabilities - generate complex structure and data attributes server-side
3. Focus on essential real-time interactions that can't be handled by the backend
4. Take an iterative approach to adding features
5. Maintain clean separation between backend and frontend responsibilities

The application uses a sophisticated data-attribute system where Django generates HTML marking each Arabic character and its corresponding diacritic position using both local indices (within words) and global indices (across the entire text). The HTML structure uses spans with data attributes like data-wd-idx for words, data-char-idx for characters, data-dia-idx for local diacritic positions, and data-global-dia-idx for global diacritic tracking.

The frontend implements two modes of operation: manual and auto-pilot. In manual mode, users navigate through words (Ctrl+Space) and characters (Space) to select positions for adding diacritical marks. In auto-pilot mode, the application automatically moves through diacritic positions sequentially using the global indices. Both modes require users to first enter edit mode (Enter key) before adding diacritics (number keys, with Ctrl+number for shadda combinations), and they can exit edit mode using the Escape key. The interaction layer is handled by AlpineJS, which manages state (wordIndex, charIndex, isEditMode, isAutoPilot, globalDiaIndex) and coordinates with utility functions for navigation and diacritic insertion.

I am a Python developer with 5+ years of experience, specializing in Django for backend development. My frontend experience is limited (less than 1 year), and I have a strong preference for minimizing JavaScript usage.

Key Characteristics:

1. Strong preference for server-side logic over client-side
2. Expert in leveraging Django's template system and context processors
3. Advocate for using HTML data attributes to encode state and behavior
4. Comfortable with AlpineJS for minimal state management and UI interactions
5. Strong belief in pushing complexity to the server where possible

Technical Preferences:

- Backend: Django with emphasis on template-driven development
- Frontend: AlpineJS for lightweight interactivity
- Programming Style: Procedural Python, minimal OOP
- Architecture: Server-driven UI, pre-computed properties in data attributes
- JavaScript: Use only when necessary, prefer declarative over imperative

Development Philosophy:

- "If it can be done in Django templates or Python, do it there"
- "Use data attributes to bridge backend and frontend"
- "Keep JavaScript minimal and declarative with AlpineJS"
- "Pre-compute as much as possible on the server"
- "Leverage Django's template system to its fullest"

When suggesting solutions:

1. Prioritize Django template solutions over JavaScript
2. Use data attributes for state and configuration
3. Keep AlpineJS code focused on simple state management
4. Prefer server-side pre-computation
5. Avoid complex JavaScript patterns or heavy client-side logic

Do not suggest:

- Complex JavaScript solutions when Django templates can handle it
- Heavy client-side frameworks (React, Vue, Angular)
- Object-oriented JavaScript patterns
- Complex state management libraries
- Client-side routing or SPA architectures
