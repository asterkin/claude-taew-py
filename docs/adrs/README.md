# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) that capture important architectural decisions made throughout the development of the claude-taew-py project.

## Purpose

ADRs serve several critical functions:

- **Documenting Rationale**: Preserve the reasoning behind architectural choices, helping current and future contributors understand why decisions were made
- **Facilitating Communication**: Provide a shared understanding of architectural principles across all user groups (app developers, adapter developers, core maintainers)
- **Supporting Evolution**: Create a historical record that enables informed decision-making as the project evolves through its phases (Python-specific → multi-language → language-agnostic)
- **AI-Accessible Knowledge**: Enable Claude Code CLI to answer "why" questions about the project's architecture and design choices

## Table of Contents

| ADR Number | Title | Status |
|------------|-------|--------|
| [ADR-0000](adr-0000-use-adrs-to-document-architecturally-significant-decisions.md) | Use ADRs to Document Architecturally Significant Decisions | Accepted |
| [ADR-0001](adr-0001-use-ai-assisted-tooling-for-adr-creation.md) | Use AI-Assisted Tooling for ADR Creation | Accepted - Phase 1 (Skill) - 2025-01-16 |
| [ADR-0002](adr-0002-create-claude-code-cli-plugin-for-taew-development.md) | Create Claude Code CLI Plugin for taew Development | Accepted |
| [ADR-0003](adr-0003-use-context7-mcp-for-documentation-access.md) | Use Context7 MCP for Documentation Access | Accepted |

---

This table will be updated as new ADRs are added to the project.

For more information about ADRs, see Michael Nygard's article on [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
