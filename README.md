# Arabic Text Diacritization Web Application

I'm working on a learning project to build an Arabic text diacritization web application. As a Python developer with 5+ years of experience but limited front-end knowledge (<1 year), I'm using Django for the backend and AlpineJS for the front end. My approach prioritizes keeping JavaScript code minimal while achieving necessary real-time interactivity.

## Project Overview

The application's core purpose is to enable fast, streamlined addition of diacritical marks (تشكيل) to Arabic text. The architecture employs a hybrid approach:

1. **Backend (Django)**: 
   - Serves pre-structured HTML with comprehensive data attributes
   - Generates structured dictionaries (wd_dict, char_dict_global, char_dict_local) for efficient data access
   - Pre-computes indices and relationships between text elements

2. **Frontend (AlpineJS/JS)**:
   - Handles essential real-time interactions (keyboard navigation, diacritic insertion)
   - Accesses structured data via JSON-parsed dictionaries
   - Uses data attributes for DOM manipulation and visual state

### Data Transfer Strategy

The application uses two complementary approaches for backend-frontend data transfer:

1. **Data Attributes**: 
   - HTML elements are marked with attributes like `data-wd-idx`, `data-char-idx`, `data-dia-idx`, and `data-global-dia-idx`
   - Used primarily for DOM selection and visual state management
   - Enables quick element lookup and state indication

2. **JSON-Serialized Dictionaries**:
   - `wd_dict`: Word-level information (isWord flag, diacritic count)
   - `char_dict_global`: Character information indexed by global position
   - `char_dict_local`: Character information indexed by word and character position
   - Enables efficient data lookup without DOM traversal
   - Provides rich metadata for validation and navigation logic

### Operation Modes

The frontend implements two modes of operation:

1. **Manual Mode**:
   - Word navigation (Ctrl+Space)
   - Character navigation (Space)
   - User-controlled position selection

2. **Auto-pilot Mode**:
   - Automatic sequential navigation through diacritic positions
   - Uses global indices for position tracking
   - Streamlined input workflow

Both modes require entering edit mode (Enter key) before adding diacritics (number keys, with Ctrl+number for shadda combinations). Users can exit edit mode using the Escape key.

## Development Philosophy

As a Python/Django developer with limited frontend experience, my approach emphasizes:

1. **Server-Side First**:
   - Push complexity to Django where possible
   - Pre-compute relationships and metadata
   - Generate structured data server-side

2. **Minimal JavaScript**:
   - Use AlpineJS for state management
   - Keep client-side code declarative
   - Focus on essential real-time interactions

3. **Hybrid Data Strategy**:
   - Use data attributes for DOM-related operations
   - Use structured dictionaries for complex data relationships
   - Keep data access efficient and organized

4. **Clean Architecture**:
   - Clear separation of concerns
   - Well-defined data flow
   - Maintainable and extensible design

## Technical Preferences

- **Backend**: Django with emphasis on template-driven development
- **Frontend**: AlpineJS for lightweight interactivity
- **Programming Style**: Procedural Python, minimal OOP
- **Architecture**: Server-driven UI with hybrid data transfer
- **JavaScript**: Use only when necessary, prefer declarative patterns

## Solution Guidelines

When suggesting solutions:

1. Prioritize Django template solutions over JavaScript
2. Leverage both data attributes and structured dictionaries appropriately
3. Keep AlpineJS code focused on simple state management
4. Prefer server-side pre-computation
5. Avoid complex JavaScript patterns

## What to Avoid

- Complex JavaScript solutions when Django templates can handle it
- Heavy client-side frameworks (React, Vue, Angular)
- Object-oriented JavaScript patterns
- Complex state management libraries
- Client-side routing or SPA architectures

This project demonstrates how to build interactive web applications while maintaining a backend-centric approach, using a hybrid data strategy to balance performance and maintainability.