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

## Tool Documentation Access (CRITICAL)

**ALWAYS query tool documentation in these scenarios:**

1. **Before using Python 3.14+ features**
2. **Before using Claude Code CLI features**
3. **When encountering errors with configured tools**
4. **When user asks "How do I... <tool-name>..." questions**

Invoke the **doc-query skill** for up-to-date documentation access.

### When Introducing New Tools

When adopting new tool(s):

1. **Document decision** - Create or update ADR justifying tool selection (ask clarifying questions if needed)
2. **Enable documentation** - Add each tool to `.claude/doc-sources.toml` via add-doc skill

Skills should invoke automatically based on context.

### Why This Matters

Training data may be outdated for:
- Python 3.14+ (released after training cutoff)
- Claude Code CLI (rapidly evolving)
- Modern tools (ruff, uv, mypy, etc.)

Context7 provides **real-time access** to current documentation.

See [ADR-0003](docs/adrs/adr-0003-use-context7-for-documentation-access.md) for architectural rationale.

## Responsibility Matrix

| Component | Purpose | Model | Example |
|-----------|---------|-------|---------|
| CLAUDE.md (this file) | Static architecture knowledge | N/A | Core patterns, design principles |
| Skills | Reusable procedures with context | Sonnet | doc-query, adr, add-doc |
| Slash Commands | User-facing workflow shortcuts | Routing | /taew-init, /taew-port |
| Scripts | Validation, verification | Local | update-adr-toc, query, list-sources |
| Sub-agents | Delegated boilerplate tasks | Haiku | Adapter scaffolding (future) |
| Config | Model selection, preferences | N/A | .claude/doc-sources.toml |

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
