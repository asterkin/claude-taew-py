# ADR Creation Skill

## Description

Guides the creation of Architecture Decision Records (ADRs) following project standards. Provides template, process guidance, and best practices for documenting architecturally significant decisions.

## When to Use This Skill

Invoke this skill when:
- Making decisions that affect system structure, quality attributes, or dependencies
- Choosing between competing technical approaches with long-term implications
- Establishing patterns or conventions for the project
- Resolving technical uncertainty or debate
- Making decisions that are expensive to change later

## ADR Creation Process

### Step 1: Determine Next ADR Number

1. Check existing ADRs in `docs/adrs/` directory
2. Find the highest numbered ADR (e.g., `adr-0005-...`)
3. Increment by 1 and zero-pad to 4 digits (e.g., `adr-0006`)

### Step 2: Create ADR File

1. Use the template below
2. Name the file: `adr-NNNN-brief-descriptive-title.md`
3. Place in: `docs/adrs/`

### Step 3: Update ADR Table of Contents

**Option A (Automated - Preferred):**
Run the TOC update script:
```bash
python scripts/update-adr-toc.py
```

**Option B (Manual):**
1. Add entry to `docs/adrs/README.md` table
2. Include: ADR number, title (linked), and status
3. Maintain sequential order

The automated script saves tokens by handling mechanical TOC updates without AI assistance.

### Step 4: Reference from Other Docs (if needed)

- Update CLAUDE.md if the decision affects AI context
- Update README.md if the decision affects users/contributors

## ADR Template

```markdown
# ADR-NNNN: [Brief Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Context

[Describe the problem, situation, or forces that led to this decision. Include:
- What architectural challenge or question prompted this decision?
- What constraints or requirements exist?
- What are the key stakeholders or affected components?
- Why is this decision architecturally significant?]

## Decision

[State the decision clearly and concisely. Include:
- What approach was chosen?
- Key requirements or principles guiding the decision
- Phased implementation plan (if applicable)
- Any specific patterns, tools, or conventions adopted]

## Consequences

### Positive

[What benefits does this decision provide?
- Improved capabilities
- Better alignment with goals
- Reduced complexity or risk]

### Negative

[What drawbacks or costs does this decision introduce?
- Additional overhead or complexity
- Limitations or constraints
- Trade-offs accepted]

### Neutral

[Other implications worth noting:
- Things that could be positive or negative depending on context
- Cultural or process changes required
- Areas requiring ongoing attention]

## References

[Optional: Links to related ADRs, external articles, documentation, or discussions]

**Link Format Examples**:
- Other ADRs: `[ADR-NNNN: Title](adr-NNNN-filename.md)`
- Project docs: `[README.md - Section](../../README.md#section-anchor)`
- Skills: `[Skill Name](../../.claude/skills/skill-name/SKILL.md)`
- Scripts: `[Script Name](../../scripts/script-name.py)`
- External: `[Article Title](https://example.com/article)`

**Note**: Use proper markdown links for navigation, not plain text references.
```

## Best Practices

### Writing Good ADRs

1. **Be Concise**: ADRs should be readable in 5-10 minutes
2. **Focus on "Why"**: Explain rationale, not just "what" was decided
3. **Capture Context**: Future readers won't have the conversation context
4. **Include Alternatives**: Briefly mention options considered and why they were rejected
5. **Acknowledge Trade-offs**: Every decision has costs and benefits
6. **Write Before/During Implementation**: Don't wait until after
7. **Keep Immutable**: Rarely edit after acceptance; supersede instead

### Common Pitfalls to Avoid

- Writing ADRs after decisions are implemented (loses context)
- Being too verbose (ADRs are not architecture documentation)
- Omitting alternatives considered (loses decision rationale)
- Not updating status when decisions change
- Creating ADRs for trivial decisions (use judgment)

### Updating and Superseding ADRs

When a decision changes:
1. Create a new ADR documenting the new decision
2. Update the old ADR's status to "Superseded by ADR-XXXX"
3. Link between related ADRs
4. Don't delete or heavily modify old ADRs (history matters)

## Example Prompts for Common ADR Types

### Technology Selection
```
Create an ADR for choosing [Technology X] over [Technology Y] for [purpose].

Context includes:
- Current requirements: [list]
- Evaluation criteria: [performance, community, licensing, etc.]
- Alternatives considered: [list]
- Key trade-offs: [describe]
```

### Pattern Adoption
```
Create an ADR for adopting [Pattern Name] pattern for [specific use case].

Context includes:
- Problem it solves: [describe]
- Where it applies: [scope]
- Alternatives considered: [list]
- Migration strategy: [if applicable]
```

### Deprecation Decision
```
Create an ADR for deprecating [feature/component/approach].

Context includes:
- Current state and limitations: [describe]
- Replacement approach: [describe]
- Migration path: [describe]
- Timeline: [if applicable]
```

### Architectural Boundary
```
Create an ADR for establishing [boundary/interface/contract].

Context includes:
- Components involved: [list]
- Interaction patterns: [describe]
- Stability requirements: [describe]
- Evolution strategy: [describe]
```

### Tooling or Process
```
Create an ADR for introducing [tool/process] to address [problem].

Context includes:
- Current pain points: [describe]
- How it addresses the problem: [describe]
- Integration approach: [describe]
- Evolution path: [if phased]
```

## Evolution of This Skill

This skill is part of a phased approach to ADR tooling (see ADR-0001):

- **Phase 1 (Current)**: Skill provides template and process guidance
- **Phase 2 (Future)**: `/adr-new` slash command for quick invocation
- **Phase 3 (Future)**: Haiku sub-agent for drafting boilerplate
- **Phase 4 (Future)**: Hooks to detect architecture changes without ADRs

Status updates will be reflected in ADR-0001.

## Usage Example

**User:** "I want to document the decision to use Context7 MCP for documentation access"

**Claude (using this skill):**
1. Checks `docs/adrs/` for existing ADRs (finds ADR-0000, ADR-0001)
2. Determines next number: ADR-0002
3. Creates `docs/adrs/adr-0002-use-context7-mcp-for-documentation-access.md`
4. Fills template with provided context
5. Updates `docs/adrs/README.md` table of contents
6. Confirms completion with user
