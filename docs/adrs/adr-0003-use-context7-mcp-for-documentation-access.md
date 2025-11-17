# ADR-0003: Use Context7 for Documentation Access

**Status:** Accepted - Implemented as Skills with TOML Configuration (2025-01-17)

## Context

### The Training Data Lag Problem

AI coding assistants, including Claude Code, are trained on data up to a specific cutoff date. This creates challenges when working with:

1. **Python 3.14+**: Released after most LLM training cutoffs
   - New language features (e.g., type parameter syntax, new stdlib modules)
   - API changes and deprecations
   - Performance characteristics and best practices
   - Rapidly evolving PEP implementations

2. **Claude Code CLI**: Actively developed tool with frequent updates
   - New features and capabilities (Skills, MCP, slash commands)
   - API and configuration changes
   - Best practices for plugin development
   - Tool-specific patterns and conventions

### Impact on All User Groups

The documentation gap affects all three user archetypes:

**Application Developers:**
- Need current Python 3.14+ APIs for building with taew-py
- Must understand latest async patterns, type hints, stdlib features
- Risk using deprecated or outdated approaches

**3rd-Party Adapter Developers:**
- Need Python 3.14+ documentation for external adapter projects
- Must follow current best practices for packaging and dependencies
- Require up-to-date integration patterns

**Core Library Maintainers:**
- Need bleeding-edge Python 3.14+ features for taew-py itself
- Must track language evolution for library design decisions
- Require accurate API documentation for stdlib adapters

**Plugin Developers (Meta-Level):**
- Need current Claude Code CLI documentation to build this plugin
- Must understand latest MCP capabilities and patterns
- Require up-to-date skill/command/agent conventions

### Traditional Solutions Are Insufficient

**1. Rely on Base LLM Training Data**
- Outdated: Training cutoff predates Python 3.14 and recent Claude Code features
- Incomplete: Missing new APIs, patterns, best practices
- Risk: AI suggests deprecated or non-existent features

**2. Manual Documentation Lookup**
- Breaks AI workflow: User must leave Claude Code to search docs
- Inefficient: Context switching between AI and browser
- Error-prone: Must copy/paste information back to AI
- Lost context: AI doesn't see the documentation directly

**3. Embedded Static Documentation**
- Becomes stale: Requires plugin updates for doc changes
- Bloat: Including full docs in plugin increases size
- Maintenance burden: Tracking and updating embedded docs
- Version mismatch: Plugin docs may lag behind actual library versions

### MCP as a Solution

The Model Context Protocol (MCP) enables AI assistants to access real-time external data sources. MCP servers can:
- Fetch current documentation on-demand
- Provide fresh information without training data updates
- Integrate seamlessly into AI workflows
- Support multiple documentation sources simultaneously

**Context7** is an MCP server specifically designed for documentation access, with:
- High-quality documentation sources (official docs, not scraped)
- Semantic search capabilities
- Support for version-specific documentation
- Token-efficient retrieval (returns relevant excerpts, not entire docs)

## Decision

Use **Context7** to provide real-time access to up-to-date documentation for Python 3.14+ and Claude Code CLI through **Skills with TOML-based configuration**.

### Implementation Evolution

**Phase 1 (MCP Server):**
- Used Context7 MCP server via npx (@upstash/context7-mcp)
- Separate process communication via stdio
- Issue: Server wrote startup messages to stderr (false positive error)

**Phase 2 (Code Execution):**
- Direct API calls via Python code
- Agent wrote Python to query and process documentation locally
- Issue: Confused user intent (skill invocation vs code generation)

**Phase 3 (Skills - Final):**
- **doc-query skill**: Query documentation from configured sources
- **add-doc skill**: Add new documentation sources to configuration
- **TOML-based configuration** (`.claude/doc-sources.toml`)
- **Token-efficient**: 0 Sonnet tokens for queries (local Python script execution)

### Skills-Based Architecture

**Directory Structure:**
```
.claude/
├── doc-sources.toml              # TOML configuration mapping tools to Context7 IDs
├── skills/
│   ├── doc-query/                # Query documentation
│   │   ├── SKILL.md
│   │   ├── lib/
│   │   │   ├── __init__.py
│   │   │   ├── context7_client.py    # Generic Context7 API client
│   │   │   └── get_library.py        # Library resolution
│   │   └── scripts/
│   │       ├── query                  # Query documentation
│   │       └── list-sources           # List available sources
│   └── add-doc/                  # Add documentation sources
│       ├── SKILL.md
│       ├── scripts/
│       │   └── add-source            # Add new source to TOML
│       └── templates/
│           └── source-entry.toml     # TOML entry template
```

**Configuration Example (`.claude/doc-sources.toml`):**
```toml
[sources.python]
context7_id = "websites/python_3_14"
description = "Python 3.14+ standard library and language features"
default_tokens = 3000
aliases = ["py", "python3"]

[sources.claude-code]
context7_id = "websites/code_claude"
description = "Claude Code CLI - skills, agents, hooks, MCP integration"
default_tokens = 2500
aliases = ["claude", "cli"]
```

**Skill Usage Examples:**

**Query documentation:**
```bash
.claude/skills/doc-query/scripts/query python "async context managers"
.claude/skills/doc-query/scripts/query claude-code "create skill" 2000
.claude/skills/doc-query/scripts/list-sources
```

**Add new documentation source:**
```bash
.claude/skills/add-doc/scripts/add-source ruff websites/ruff "Ruff Python linter" --tokens 2000 --alias ruff-lint
```

**Documentation Sources:**
- Configured via `.claude/doc-sources.toml` (extensible for any Context7 library)
- Initial sources: `python` (Python 3.14+), `claude-code` (Claude Code CLI)
- Add more sources via add-doc skill (ruff, mypy, pytest, etc.)

**Integration Points:**
- Skills invoked explicitly by Sonnet agent
- Scripts execute locally (Python 3.12+ stdlib only - urllib, tomllib, pathlib)
- Progressive disclosure: query only when needed
- Token-efficient: 0 Sonnet tokens (local script execution)

### Setup Requirements

**For Contributors:**
1. Obtain Context7 API key from [context7.com](https://context7.com)
2. Set `CONTEXT7_API_KEY` environment variable in shell config
3. No external dependencies required - uses Python 3.12+ stdlib only (urllib)

**Token Economics:**
- Skills approach achieves **0 Sonnet tokens** for documentation queries
- Local Python script execution (pre-approved permissions)
- More efficient than:
  - Traditional MCP (all data passes through model)
  - Sub-agents with Haiku (still consumes tokens for filtering)
  - AI hallucinating outdated information (requires correction/rework)
  - User manually looking up and pasting documentation (context switching)
  - Embedding full docs in prompts (massive token waste)

## Consequences

### Positive

1. **Overcomes Training Data Lag**: Access to current Python 3.14+ and Claude Code CLI documentation
2. **Benefits All User Groups**: App developers, adapter developers, core maintainers, and plugin developers
3. **Seamless Workflow**: Documentation lookup happens in-context, no browser switching
4. **Always Current**: Documentation updates don't require plugin releases
5. **Version-Specific**: Can access docs for specific Python/library versions
6. **Zero Sonnet Tokens**: 0 tokens for documentation queries (local script execution with pre-approved permissions)
7. **Skills Composition**: Explicit skill invocation (no "magic" hooks), follows Claude Code patterns
8. **Multi-Source**: Can query Python, Claude Code, and any Context7-supported library
9. **Extensible**: TOML-based configuration - add new sources via add-doc skill
10. **No External Dependencies**: Uses Python 3.12+ stdlib only (urllib, tomllib, pathlib) - aligns with taew-py philosophy
11. **Skill Encapsulation**: Self-contained skills with scripts/lib/templates in dedicated directories
12. **Alias Support**: Convenient short names (py → python, claude → claude-code)

### Negative

1. **External Dependency**: Requires Context7 service availability
2. **API Key Required**: Contributors must sign up and configure key (friction in setup)
3. **Network Dependency**: Offline development loses documentation access
4. **Service Risk**: Dependent on Context7 service continuity and pricing
5. **Manual Source Discovery**: Must browse Context7 to find library IDs (not searchable via API)

### Neutral

1. **Configuration Overhead**: One-time setup per contributor
2. **Another Service**: Adds to stack (Context7 + Claude + Anthropic API)
3. **Documentation Quality**: Depends on Context7's source curation and indexing
4. **Rate Limits**: Subject to Context7's API rate limits and quotas
5. **Privacy**: Documentation queries sent to external service

## Alternatives Considered

### 1. Rely on Base LLM Training Data
**Rejected**: Python 3.14 and recent Claude Code features not in training data; leads to outdated or incorrect suggestions.

### 2. Manual Documentation Lookup
**Rejected**: Breaks AI workflow, inefficient context switching, AI doesn't see documentation directly.

### 3. Embedded Static Documentation
**Rejected**: Becomes stale, bloats plugin, maintenance burden, version mismatch issues.

### 4. Web Search / WebFetch Tool
**Rejected**: Less reliable than curated documentation sources, token-heavy (full pages), search quality varies, harder to target specific versions.

### 5. Other Documentation MCP Servers
**Considered**: Context7 chosen for:
- High-quality official documentation sources
- Good Python and Claude Code coverage
- Semantic search capabilities
- Active maintenance and support

### 6. Build Custom MCP Server
**Rejected**: Significant development and maintenance overhead; Context7 already solves this problem well.

### 7. Cache Documentation Locally
**Rejected**: Still becomes stale, requires update mechanism, duplicates Context7's functionality.

## Future Considerations

### Documentation Source Evolution

As the plugin evolves, additional documentation sources may be valuable:
- **Phase 2** (Multi-language): TypeScript, Rust, etc. documentation
- **3rd-Party Libraries**: AWS SDK, GCP SDK, PostgreSQL driver docs
- **taew-py Itself**: Once taew-py documentation is substantial

Context7's multi-source capability supports this evolution without architectural changes.

### Offline Fallback

If offline development becomes important:
- Could implement graceful degradation (fallback to training data)
- Could cache frequent queries (trade-off: staleness vs. offline capability)
- Could document "offline mode" limitations

Not implementing now (YAGNI), but architecture allows for future enhancement.

## References

- [CLAUDE.md - Tool Documentation Access](../../CLAUDE.md#tool-documentation-access-critical)
- [.claude/doc-sources.toml](../../.claude/doc-sources.toml) - Documentation sources configuration
- [doc-query skill](../../.claude/skills/doc-query/SKILL.md) - Query documentation
- [add-doc skill](../../.claude/skills/add-doc/SKILL.md) - Add documentation sources
- [Context7](https://context7.com) - Documentation provider
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ADR-0002: Create Claude Code CLI Plugin](adr-0002-create-claude-code-cli-plugin-for-taew-development.md) - Establishes need for up-to-date documentation access
