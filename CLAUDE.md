# claude-taew-py

Claude Code CLI plugin for AI-assisted development with taew-py Ports & Adapters foundation library.

## Project Context

**taew-py** is a Python 3.14+ foundation library that makes Ports & Adapters (Hexagonal Architecture) natural and fast, enabling rapid development of Minimal Evolvable Products (MEPs) for early-stage startups.

**claude-taew-py** is an AI-native plugin that teaches Claude Code how to scaffold and develop taew-py applications and 3rd party technology adapters as well as maintaining taew-py itself efficiently.

## Strategic Background

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
- **Documentation Access**: Context7 MCP server for up-to-date Python 3.14+ and Claude Code CLI documentation

**Why Documentation Access Matters**: Both Python 3.14+ and Claude Code CLI are rapidly evolving and may not be well-represented in base LLM training data. Context7 enables real-time lookup of current documentation, benefiting all three user groups (app developers, adapter developers, core maintainers) as well as this plugin's own development.

## Responsibility Matrix

| Component | Purpose | Model | Example |
|-----------|---------|-------|---------|
| CLAUDE.md (this file) | Static architecture knowledge | N/A | Core patterns, design principles |
| Skills | Reusable procedures with context | Sonnet | "Create port following pattern" |
| Slash Commands | User-facing workflow shortcuts | Routing | /taew-init, /taew-port |
| Scripts | Validation, verification | Local | make test, type checking |
| Sub-agents | Delegated boilerplate tasks | Haiku | Generate adapter scaffolding |
| Config | Model selection, preferences | N/A | Which model for what task |

**Key principle**: Each layer reduces token waste at the layer above.

## Project Structure Philosophy

This plugin should mirror taew-py's philosophy at the meta-level:
- Core patterns are technology-neutral
- Implementation details are adapters
- Claude integration itself is "just another adapter layer"

---

For detailed taew-py architectural principles, see: https://github.com/asterkin/taew-py
