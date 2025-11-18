# ADR-0005: Python Code Standards and Style Guide

**Status:** Accepted

## Context

This plugin generates Python code through AI assistance and must maintain high quality standards:

1. **Python 3.14+ modern features**:
   - Training data may predate Python 3.9+ built-in generic types
   - Modern type hints improve readability and IDE support
   - Legacy `typing` module imports create unnecessary noise

2. **Type safety requirements**:
   - VSCode with Pylance (strict mode) is the default IDE
   - Type errors prevent code from working correctly
   - AI-generated code must pass type checking without manual fixes

3. **AI code generation consistency**:
   - Multiple AI sessions should produce similar code for similar tasks
   - Standards reduce debugging time for generated code
   - Explicit patterns help Claude learn project preferences

4. **taew-py philosophy alignment**:
   - Prefer explicit over implicit
   - Favor composition and clarity
   - Minimize boilerplate without sacrificing readability

This decision establishes Python coding standards that ensure consistent, type-safe, modern Python code generation.

## Decision

### 1. Type Hints - Use Modern Built-in Types (Python 3.9+)

**DO** use built-in generic types:
```python
✅ GOOD:
def process_items(items: list[str]) -> dict[str, int]:
    mapping: dict[str, int] = {}
    for item in items:
        mapping[item] = len(item)
    return mapping

def get_optional_value(key: str) -> str | None:
    return cache.get(key)
```

**DON'T** use `typing` module for standard generics:
```python
❌ BAD:
from typing import List, Dict, Optional

def process_items(items: List[str]) -> Dict[str, int]:
    mapping: Dict[str, int] = {}
    ...

def get_optional_value(key: str) -> Optional[str]:
    ...
```

**Rationale**:
- Python 3.9+ allows `list[T]`, `dict[K, V]`, etc. without imports
- `X | None` is clearer than `Optional[X]`
- Reduces imports, improves readability
- Aligns with modern Python community standards

**Exceptions**: Use `typing` module for:
- `Protocol`, `TypeVar`, `Callable` (no built-in equivalents)
- Complex type constructs not available as built-ins

### 2. Prefer Comprehensions Over Imperative Loops

**DO** use comprehensions for transformations:
```python
✅ GOOD:
# List comprehension
active_users = [user for user in users if user.is_active]

# Dict comprehension
user_map = {user.id: user.name for user in users}

# Set comprehension
unique_ids = {user.id for user in users}
```

**DON'T** use imperative loops for simple transformations:
```python
❌ BAD:
# Imperative list building
active_users = []
for user in users:
    if user.is_active:
        active_users.append(user)

# Imperative dict building
user_map = {}
for user in users:
    user_map[user.id] = user.name
```

**Rationale**:
- More concise and readable
- Expresses intent (transformation) directly
- Often more performant
- Pythonic idiom

**Exceptions**: Use loops when:
- Logic is complex (multiple conditions, nested operations)
- Side effects are involved (I/O, logging)
- Early termination is needed

### 3. Type Safety - Code Must Pass Pylance Strict Mode

**DO** type comparison method parameters correctly:
```python
✅ GOOD:
from typing import Any

class Rate:
    def __init__(self, amount: float):
        self.amount = amount

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rate):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Rate):
            return NotImplemented
        return self.amount < other.amount
```

**DON'T** use incorrect types or skip type guards:
```python
❌ BAD:
class Rate:
    def __eq__(self, other: Rate) -> bool:  # Too specific - breaks Liskov
        return self.amount == other.amount

    def __lt__(self, other: Any) -> bool:  # No type guard
        return self.amount < other.amount  # Runtime error if other.amount missing
```

**Rationale**:
- Comparison operators must accept `object` parameter (Liskov Substitution Principle)
- Type guards prevent runtime errors
- `NotImplemented` allows Python to try reverse comparison
- Pylance strict mode catches these errors

**Pattern**: Always use type guards in comparison methods:
```python
if not isinstance(other, MyClass):
    return NotImplemented
```

### 4. Executable Scripts - Shebang + Executable Permission

**DO** make scripts directly executable:
```python
#!/usr/bin/env python3
"""
Script description here.
"""

def main() -> None:
    # Script logic
    pass

if __name__ == "__main__":
    main()
```

```bash
chmod +x script.py
./script.py  # Invoke directly
```

**DON'T** rely on `python` command:
```python
# No shebang

def main():
    pass

if __name__ == "__main__":
    main()
```

```bash
python script.py  # Requires knowing it's Python
```

**Rationale**:
- Self-documenting (shebang declares interpreter)
- Portable (`env` finds Python in PATH)
- Consistent with hook conventions
- Better user experience (just run `./script.py`)

**Pattern**:
1. Add shebang: `#!/usr/bin/env python3`
2. Make executable: `chmod +x script.py`
3. Invoke: `./script.py`

### 5. Encapsulation - Keep Utilities with Their Consumers

**DO** co-locate utilities with the code that uses them:
```
✅ GOOD:
.claude/skills/doc-query/
├── SKILL.md
└── scripts/
    ├── query.py          # Main script
    └── parser.py         # Helper used only by query.py
```

**DON'T** create global utility directories:
```
❌ BAD:
scripts/
├── doc-query-parser.py  # Pollutes global namespace
└── doc-query.py

.claude/skills/doc-query/
└── SKILL.md
```

**Rationale**:
- Improves discoverability (utilities near consumers)
- Reduces global namespace pollution
- Makes dependencies explicit
- Supports skill portability

**Exception**: Truly shared utilities used by 3+ independent components (rare in practice).

### 6. Templates - Extract Formatting from Logic

**DO** separate templates from code:
```
✅ GOOD:
.claude/skills/adr/
├── scripts/
│   └── create-adr.py     # Loads template from file
└── templates/
    └── adr-template.md   # Markdown template

# In create-adr.py:
template_path = Path(__file__).parent.parent / "templates" / "adr-template.md"
template_content = template_path.read_text()
```

**DON'T** embed templates in Python strings:
```python
❌ BAD:
# In create-adr.py:
ADR_TEMPLATE = """# ADR-{number}: {title}

**Status:** {status}

## Context
...
"""
```

**Rationale**:
- Separates presentation from logic
- Makes templates easier to edit (markdown syntax highlighting)
- Reduces code clutter
- Non-programmers can update templates

**Pattern**: Store templates in `templates/` subfolder within skill directory.

## Consequences

### Positive

1. **Consistent code generation**: AI produces similar code across sessions
2. **Type safety**: Pylance strict mode catches errors before runtime
3. **Modern Python**: Uses latest language features and idioms
4. **Better IDE support**: Built-in types have better autocomplete
5. **Reduced debugging**: Standards prevent common errors
6. **Easier code review**: Consistent patterns are easier to verify
7. **Self-documenting**: Patterns like shebang + chmod are explicit

### Negative

1. **Learning curve**: Contributors must learn project conventions
2. **Discipline required**: Easy to fall back to old habits (`List` instead of `list`)
3. **Refactoring burden**: Existing code may need updates to match standards

### Neutral

1. **Tooling enforcement**: Requires ruff + pyright to validate (future: ADR for tooling setup)
2. **Documentation maintenance**: This ADR must stay current with Python evolution
3. **Training updates**: May need to retrain Claude on new patterns

## References

- [ADR-0004: Project Structure and Documentation Standards](adr-0004-project-structure-and-documentation-standards.md) - Where to organize code and docs
- [Python 3.9+ PEP 585](https://peps.python.org/pep-0585/) - Type Hinting Generics In Standard Collections
- [Python 3.10+ PEP 604](https://peps.python.org/pep-0604/) - Allow writing union types as `X | Y`
- [CLAUDE.md - Python Code Standards](../../CLAUDE.md#python-code-standards) - Quick reference for AI context

---

**Date**: 2025-01-18
**Supersedes**: None
**Related to**: ADR-0004 (project structure)
