# ADR-0004: Project Structure and Documentation Standards

**Status:** Accepted

## Context

As an AI-native plugin for Claude Code CLI, this project faces unique documentation challenges:

1. **Multiple audiences** with different needs:
   - End users discovering the plugin (need quick start)
   - Contributors developing the plugin (need setup and patterns)
   - Strategic stakeholders planning features (need vision and rationale)
   - AI assistant (needs operational directives, loaded every session)

2. **Token efficiency is critical**:
   - CLAUDE.md is read on every conversation start
   - Skills inherit conversation context
   - Redundant content wastes tokens and increases costs
   - Bloated context reduces response quality

3. **Documentation drift prevention**:
   - Duplicate information across files gets out of sync
   - Contributors don't know where to document decisions
   - Unclear ownership leads to incomplete updates

4. **Code organization principles**:
   - Skills should be self-contained modules
   - Utilities belong with their consumers (not globally)
   - Templates should be separated from logic
   - Project structure reflects architectural patterns

This decision establishes clear boundaries for documentation responsibility and code organization to address these challenges.

## Decision

### Documentation Responsibilities

Establish single-source-of-truth principle with strict file boundaries:

| File | Audience | Purpose | Scope | Token Budget |
|------|----------|---------|-------|--------------|
| **README.md** | End users, first-time visitors | Discovery and quick start | Installation, basic usage examples, navigation to other docs | ~30-40 lines |
| **CONTRIBUTING.md** | Contributors, maintainers | Development setup and workflow | Prerequisites, git workflow, testing, operational guidelines reference | ~100-150 lines |
| **VISION.md** | Strategic stakeholders, planners | Long-term direction and philosophy | Project goals, use cases, roadmap, architectural philosophy | Unbounded |
| **CLAUDE.md** | AI assistant (every session) | Critical operational directives | Tool activation, coding standards reminders, DO NOT warnings, references to other docs | ~50-70 lines |
| **ADRs** | Decision archaeology | Architectural rationale | "Why" behind specific choices, alternatives considered, consequences | Per-decision (~200-400 lines) |
| **CODE_OF_CONDUCT.md** | Community members | Behavioral guidelines | Participation expectations, enforcement | Standard template |
| **LICENSE** | Legal / users | Legal terms | Usage rights, restrictions | Standard template |

### Code Structure Patterns

#### 1. Skills Are Self-Contained Modules

```
.claude/skills/<skill-name>/
├── SKILL.md              # Skill documentation
├── scripts/              # Skill-specific scripts
│   ├── helper-1.py
│   └── helper-2.py
└── templates/            # Skill-specific templates
    └── template.md
```

**Rationale**: Skills are portable, reusable components. All dependencies should live within the skill directory.

**Anti-pattern**: Global `scripts/` folder at project root (violates encapsulation)

#### 2. Utilities Live with Consumers

```
✅ GOOD: .claude/skills/doc-query/scripts/query.py
❌ BAD:  scripts/doc-query-helper.py
```

**Rationale**: Co-location improves discoverability and reduces global namespace pollution.

#### 3. Templates Extracted from Logic

```
✅ GOOD:
  - Logic: .claude/skills/adr/scripts/create-adr.py
  - Template: .claude/skills/adr/templates/adr-template.md

❌ BAD: Template content embedded in Python strings
```

**Rationale**: Separates presentation from business logic, makes templates easier to edit.

**Note**: For detailed Python coding conventions (including how to write these scripts), see [ADR-0005: Python Code Standards](adr-0005-python-code-standards.md).

### Cross-Reference Conventions

**Navigation graph direction** (prevents circular references):

```
README.md ──→ VISION.md, CONTRIBUTING.md, ADRs
              ↓
CONTRIBUTING.md ──→ CLAUDE.md, ADRs
                    ↓
VISION.md ──→ ADRs
            ↓
CLAUDE.md ──→ VISION.md, ADRs (leaf node - nothing points back)
              ↓
ADRs ──→ other ADRs
```

**Critical rule**: CLAUDE.md is a **leaf node** in the reference graph:
- Everyone can point TO CLAUDE.md
- CLAUDE.md points to others (VISION, ADRs)
- But nothing CLAUDE.md references should point back to it (prevents circular loading)

**Link format**: Always use markdown links with section anchors:
```markdown
✅ GOOD: See [VISION.md - AI-Native Architecture](VISION.md#ai-native-architecture)
❌ BAD:  See VISION.md for details
```

**Avoid duplication**: Prefer "refer, don't repeat"
```markdown
✅ GOOD: For strategic context, see [VISION.md](VISION.md)
❌ BAD:  [Copies entire strategic context into CLAUDE.md]
```

## Consequences

### Positive

1. **Token efficiency**: CLAUDE.md reduced from ~165 lines to ~50 lines (~70% reduction in context per session)
2. **Clear ownership**: Contributors know exactly where to document information
3. **No duplication**: Single source of truth for each type of content
4. **Better navigation**: Progressive disclosure - readers find what they need without noise
5. **Maintainability**: Updates happen in one place, reducing drift
6. **Portability**: Skills are self-contained, easy to share/reuse
7. **Scalability**: Structure handles project growth (more skills, more docs)

### Negative

1. **Navigation overhead**: Readers must follow references between files (mitigated by clear links)
2. **Discipline required**: Contributors must resist duplicating content (mitigated by this ADR + code review)
3. **Initial learning curve**: New contributors need to learn the structure (mitigated by CONTRIBUTING.md)
4. **More files**: More places to look initially (mitigated by README.md as hub)

### Neutral

1. **Requires periodic audits**: Check for documentation drift and broken links
2. **Template enforcement**: Need to ensure skills follow structure conventions
3. **Reference validation**: Consider pre-commit hook to check markdown links (future enhancement)

## References

- [ADR-0003: Use Context7 for Documentation Access](adr-0003-use-context7-mcp-for-documentation-access.md) - Why token efficiency matters
- [ADR-0005: Python Code Standards](adr-0005-python-code-standards.md) - How to write Python code in this project
- [VISION.md - AI-Native Architecture](../../VISION.md#ai-native-architecture) - Component responsibility matrix
- [CLAUDE.md](../../CLAUDE.md) - Example of token-optimized operational directives
- [README.md](../../README.md) - Example of minimal entry point pattern
- [ADR-0001: AI-Assisted Tooling for ADRs](adr-0001-use-ai-assisted-tooling-for-adr-creation.md) - Skills architecture philosophy

---

**Date**: 2025-01-18
**Supersedes**: None
**Related to**: ADR-0003 (token efficiency), ADR-0005 (coding standards)
