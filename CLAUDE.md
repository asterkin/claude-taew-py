# claude-taew-py

Claude Code CLI plugin for AI-assisted development with taew-py Ports & Adapters foundation library.

## Critical Instructions

**BEFORE WORKING ON TASKS:**

1. **Strategic context?** → See [VISION.md](VISION.md) for project philosophy, use cases, and roadmap
2. **File organization?** → See [ADR-0004: Project Structure and Documentation Standards](docs/adrs/adr-0004-project-structure-and-documentation-standards.md)
3. **Python standards?** → See [ADR-0005: Python Code Standards](docs/adrs/adr-0005-python-code-standards.md)

## Project Context

**taew-py** is a Python 3.14+ foundation library that makes Ports & Adapters (Hexagonal Architecture) natural and fast, enabling rapid development of Minimal Evolvable Products (MEPs) for early-stage startups.

**claude-taew-py** is an AI-native plugin that teaches Claude Code how to scaffold and develop taew-py applications and 3rd party technology adapters as well as maintaining taew-py itself efficiently.

For detailed use cases and architectural philosophy, see [VISION.md - Target Users & Use Cases](VISION.md#target-users--use-cases) and [VISION.md - AI-Native Architecture](VISION.md#ai-native-architecture).

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

See [ADR-0003](docs/adrs/adr-0003-use-context7-mcp-for-documentation-access.md) for architectural rationale.

## Python Code Standards - Quick Reference

See [ADR-0005: Python Code Standards](docs/adrs/adr-0005-python-code-standards.md) for detailed guidelines.

**Critical reminders** (most commonly violated):

1. **Modern type hints**: Use `list[str]`, not `List[str]` (Python 3.9+ built-in types)
2. **Union types**: Use `str | None`, not `Optional[str]`
3. **Comparison methods**: Type parameter as `object`, use type guards, return `NotImplemented`
4. **Executable scripts**: Start with `#!/usr/bin/env python3` + `chmod +x`
5. **Encapsulation**: Keep utilities with consumers (`.claude/skills/*/scripts/`)
6. **Templates**: Extract to separate files (`.claude/skills/*/templates/`)

## Project Structure - Quick Reference

See [ADR-0004: Project Structure and Documentation Standards](docs/adrs/adr-0004-project-structure-and-documentation-standards.md) for detailed guidelines.

**Critical reminders**:

1. **Skills are self-contained**: All scripts/templates live in `.claude/skills/<name>/`
2. **Documentation hierarchy**: README → VISION, CONTRIBUTING, ADRs → CLAUDE (leaf node)
3. **No circular refs**: CLAUDE.md points to VISION/ADRs, but they don't point back
4. **Token budgets**: CLAUDE.md (~50-70 lines), README (~30-40 lines), VISION (unbounded)

---

For detailed taew-py architectural principles, see: https://github.com/asterkin/taew-py
