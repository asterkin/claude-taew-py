# claude-taew-py

Claude Code CLI plugin for AI-assisted development with taew-py Ports & Adapters foundation library.

## Project Context

**taew-py** is a Python 3.14+ foundation library that makes Ports & Adapters (Hexagonal Architecture) natural and fast, enabling rapid development of Minimal Evolvable Products (MEPs) for early-stage startups.

**claude-taew-py** is an AI-native plugin that teaches Claude Code how to scaffold and develop taew-py applications and 3rd party technology adapters as well as maintaining taew-py itself efficiently.

## Strategic Background

> For historical context and rationale behind architectural decisions, see [Architecture Decision Records (ADRs)](docs/adrs/README.md)

### Use Cases This Plugin Must Support

1. **Application Development**
   - Scaffolding new taew-py projects
   - Creating domain models, ports, workflows, adapters
   - CLI-first workflow automation

2. **3rd-Party Adapter Development**
   - Generating adapter skeletons for new technologies (AWS, GCP, PostgreSQL, etc.)
   - Following taew-py adapter patterns and conventions

3. **Core Library Maintenance**
   - Adding new stdlib adapters to taew-py
   - Maintaining consistency with existing patterns
   - All skills should work equally for apps, adapters, and core

**Implication**: Generated code and workflows must be reusable across all three contexts.

> For taew-py architectural principles, see [Core Philosophy](README.md#core-philosophy) in README.md

## AI-Native Implementation

> For strategic context and evolution path, see [Why AI-Native?](README.md#why-ai-native) in README.md

This plugin implements AI-native tooling through complementary mechanisms:
- **Skills**: Reusable procedures with architectural context (Sonnet)
- **Slash commands**: User-facing workflow shortcuts
- **Sub-agents**: Boilerplate generation (cost-optimized with Haiku)
- **Scripts**: Validation without AI tokens
- **Documentation Access**: Context7 code execution for up-to-date Python 3.14+ and Claude Code CLI documentation

## Using Context7 for Documentation

**IMPORTANT**: Always use the **librarian agent** for Python 3.14+ and Claude Code CLI documentation queries, as base training data may be outdated.

**Delegate to librarian agent** (Haiku - token-efficient):
```
Use the Task tool to invoke the librarian agent for documentation queries.
Example: "Query Python 3.14 async generators documentation"
```

The librarian agent:
- Uses Haiku model (1/5 cost of Sonnet)
- Queries Context7 API directly via `servers/context7/`
- Filters and processes markdown locally
- Returns only relevant excerpts

**Alternative: Direct code execution** (if you need fine-grained control):
```python
from servers.context7.search_python import search_python_docs
from servers.context7.search_claude_code import search_claude_code_docs

# Query and filter locally
docs = search_python_docs("async context managers", tokens=2000)
content = docs.get("content", "")
relevant = [line for line in content.split('\n') if "async with" in line]
```

**Why This Matters**: Python 3.14+ and Claude Code CLI evolve rapidly and may not be well-represented in base LLM training data. Librarian agent provides:
- Real-time access to current documentation
- 98.7% token savings through local filtering
- Cost-effective processing (Haiku model)
- Benefits all three user groups and this plugin's development
- See [ADR-0003](docs/adrs/adr-0003-use-context7-mcp-for-documentation-access.md) for rationale

## Responsibility Matrix

| Component | Purpose | Model | Example |
|-----------|---------|-------|---------|
| CLAUDE.md (this file) | Static architecture knowledge | N/A | Core patterns, design principles |
| Skills | Reusable procedures with context | Sonnet | "Create port following pattern" |
| Slash Commands | User-facing workflow shortcuts | Routing | /taew-init, /taew-port |
| Scripts | Validation, verification | Local | make test, type checking |
| Sub-agents | Delegated boilerplate tasks | Haiku | Librarian (docs), adapter scaffolding |
| Config | Model selection, preferences | N/A | Which model for what task |

**Key principle**: Each layer reduces token waste at the layer above.

## Python Code Standards

When writing Python code for this project:

### 1. Type Hints - Use Modern Built-in Types (Python 3.9+)
- ✅ `list[str]`, `dict[str, int]`, `tuple[int, ...]`
- ❌ `List[str]`, `Dict[str, int]`, `Tuple[int, ...]` (typing module imports)
- ✅ `str | None`
- ❌ `Optional[str]`

### 2. Prefer Comprehensions Over Imperative Loops
- ✅ `[x for x in items if condition]`
- ❌ `result = []; for x in items: if condition: result.append(x)`

### 3. Type Safety - Code Must Pass Pylance Strict Mode
- Always type comparison method parameters: `def __lt__(self, other: object) -> bool:`
- Use type guards: `if isinstance(other, MyClass):`
- Return `NotImplemented` for comparison operators when types don't match
- Explicit type narrowing: Use `if x is not None:` instead of `if x:`

### 4. Executable Scripts - Mark with Shebang + chmod
- Start with: `#!/usr/bin/env python3`
- Make executable: `chmod +x script.py`
- Invoke as: `./script.py` (not `python script.py`)
- Rationale: Self-documenting, portable, consistent with hooks

### 5. Encapsulation - Keep Utilities with Their Consumers
- ✅ `.claude/skills/my-skill/scripts/helper.py`
- ❌ `scripts/my-skill-helper.py` (pollutes project root)
- Rationale: Skills are self-contained, portable modules

### 6. Templates - Extract Formatting from Logic
- Use separate template files for formatted outputs
- Keep business logic in Python, presentation in templates
- Example: `.claude/skills/adr/templates/adr-template.md`

## Project Structure Philosophy

This plugin should mirror taew-py's philosophy at the meta-level:
- Core patterns are technology-neutral
- Implementation details are adapters
- Claude integration itself is "just another adapter layer"

---

For detailed taew-py architectural principles, see: https://github.com/asterkin/taew-py
