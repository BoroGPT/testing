# CLAUDE.md - AI Assistant Guidelines

This document provides guidance for AI assistants working with the Magic the Gathering Codex codebase.

## Project Overview

**Magic the Gathering Codex** is a simple Python-based card database and search tool for Magic the Gathering cards. It provides a CLI interface to list and search card data stored in JSON format.

- **Language:** Python 3
- **Dependencies:** None (uses only Python standard library)
- **Purpose:** Educational example of a CLI data lookup application

## Codebase Structure

```
/
├── README.md           # Project documentation and usage instructions
├── CLAUDE.md           # AI assistant guidelines (this file)
└── codex/
    ├── codex.py        # Main application script (CLI entry point)
    └── cards.json      # Card database (JSON array)
```

## Key Files

### `codex/codex.py`
The main application module containing:
- `load_cards(path)` - Loads card data from JSON file
- `list_cards(cards)` - Displays all cards in summary format
- `search_cards(cards, query)` - Case-insensitive card name search
- `main()` - CLI entry point using argparse

### `codex/cards.json`
JSON array containing card objects with this schema:
```json
{
  "name": "Card Name",
  "type": "Card Type",
  "mana_cost": "Mana Cost String",
  "text": "Card effect text",
  "set": "Set Code",
  "rarity": "Rarity Level"
}
```

## Development Commands

### Running the Application

```bash
# List all cards
python codex/codex.py list

# Search for cards by name
python codex/codex.py search <query>

# Use custom data file
python codex/codex.py list --data /path/to/cards.json
```

### Testing Changes

No automated tests exist. Verify changes manually:
```bash
python codex/codex.py list
python codex/codex.py search Lotus
python codex/codex.py search nonexistent
```

## Code Conventions

### Python Style
- Use standard library modules only (json, argparse, pathlib)
- Functional approach with separate functions for distinct operations
- Use `pathlib.Path` for cross-platform path handling
- Specify `encoding='utf-8'` when opening files
- Use `if __name__ == '__main__':` guard for entry points

### Naming
- Functions: `snake_case`
- Variables: `snake_case`
- Constants: Not used, but would be `UPPER_CASE`

### Error Handling
- Use argparse's built-in error handling for CLI validation
- Use parser.error() for validation errors (e.g., missing query)

### Output Formatting
- List command: `{name} - {type} - {mana_cost}` format
- Search command: Pretty-printed JSON with 2-space indent
- No matches: Plain text message "No matches found"

## Data Management

### Adding Cards
Add new card entries to `codex/cards.json` following the existing schema. All six fields are expected:
- `name` (string): Card name
- `type` (string): Card type (e.g., "Instant", "Artifact", "Creature")
- `mana_cost` (string): Mana cost notation (e.g., "R", "2U", "0")
- `text` (string): Card rules text
- `set` (string): Set code (e.g., "LEA", "M11")
- `rarity` (string): Rarity level (e.g., "Common", "Rare")

## Guidelines for AI Assistants

### When Modifying Code
1. Maintain the existing code style and patterns
2. Keep functions focused and single-purpose
3. Avoid adding external dependencies
4. Use pathlib for any new path operations
5. Preserve the CLI interface contract

### When Adding Features
1. Follow the existing functional architecture
2. Add new functions rather than bloating existing ones
3. Update this CLAUDE.md if adding new commands or changing structure
4. Consider backwards compatibility with existing card data

### When Fixing Bugs
1. Test with existing commands before and after changes
2. Verify JSON parsing still works correctly
3. Check both successful and error cases

### Common Tasks
- **Add a new card:** Edit `codex/cards.json`, add object to array
- **Add a new command:** Add to argparse choices, implement handler in main()
- **Change output format:** Modify `list_cards()` or search output section
- **Add new card field:** Update schema in cards.json, modify display functions
