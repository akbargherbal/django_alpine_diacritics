**## JS Refactoring Request Template**  
I need to reorganize the JavaScript code for my Django-based Arabic diacritization app while maintaining all existing functionality. The Django templates, HTML structure, data attributes (data-*), and backend-generated dictionaries (wd_dict, char_dict_*) must remain completely unchanged - we're only refactoring the JS files.

**1. Preservation Boundaries**  
*Strictly Off-Limits:*  
- Django templates & HTML structure  
- Data attributes (`data-wd-idx`, `data-dia-idx`, etc)  
- Backend dictionary format (`wd_dict`, `char_dict_global`, etc)  
- HTMX integration points  
- CSS classes/selectors  

**2. Current App Overview**  
*Core Functionality:*  
[Brief description of what the app does]  
"Web-based Arabic text diacritization tool with manual/auto modes, using predefined dictionaries from Django backend"

**3. JS Pain Points**  
```text
Current Issues:
1. All navigation logic in single 500-line utils.js
2. State variables (wordIndex/charIndex) scattered globally
3. DOM manipulation mixed with business logic
4. No clear error handling paths
5. Hard to trace mode transitions
```

**4. Refactoring Goals**  
```markdown
- [ ] Keep **all existing Django-HTML interactions** intact
- [ ] Maintain **current data attribute/DOM structure**
- [ ] Improve code discoverability without new frameworks
- [ ] Create logical separation of concerns
- [ ] Add lightweight documentation system
```

**5. Proposed JS Architecture**  
```bash
static/js/
├── core/                  # Fundamental operations
│   ├── state.js           # Central state management
│   ├── dom.js             # DOM interaction helpers
│   └── validation.js      # Shared validation logic
├── features/              # Feature modules
│   ├── navigation/        # Navigation system
│   │   ├── word.js        # Word-level navigation 
│   │   └── character.js   # Char-level navigation
│   └── diacritics/        # Diacritic management
│       ├── manual.js      # Manual mode logic
│       └── autopilot.js   # Auto-pilot logic
├── integration/           # Third-party libs
│   ├── hotkeys.js         # Keybind setup
│   └── htmx.js            # HTMX extensions
└── app.js                 # Main Alpine initialization
```

**6. Success Metrics**  
- Any dev can:  
  1. Find diacritic insertion logic in <2 minutes  
  2. Understand state flow from 30s code scan  
  3. Modify navigation without breaking validation  
- Zero HTML/Django template changes required  
- All existing keyboard shortcuts remain identical  

**7. Risk Mitigation Plan**  
1. Phase 1: Create new parallel structure  
2. Phase 2: Migrate features one-by-one  
3. Phase 3: Legacy code removal  
4. Validation: Manual QA checklist per phase  

**8. Specific Questions**  
- How to handle cross-module state access?  
- What deserves to be a pure function?  
- How to document complex keybind interactions?  
- Best way to preserve HTMX integration?  

