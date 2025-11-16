# ADR-0003: Use Context7 MCP for Documentation Access

**Status:** Accepted

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

Use **Context7 MCP server** to provide real-time access to up-to-date documentation for Python 3.14+ and Claude Code CLI.

### Implementation

**Configuration** (`.mcp.json`):
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}",
        "CONTEXT7_SOURCES": "python-docs,claude-code-docs"
      }
    }
  }
}
```

**Documentation Sources:**
- `python-docs`: Official Python 3.14+ documentation
- `claude-code-docs`: Official Claude Code CLI documentation

**Integration Points:**
- Skills can reference current API documentation
- AI can lookup unfamiliar Python 3.14+ features during code generation
- Plugin development benefits from current Claude Code best practices
- Users can ask "how does X work in Python 3.14?" and get accurate answers

### Setup Requirements

**For Contributors:**
1. Obtain Context7 API key from [context7.com](https://context7.com)
2. Set `CONTEXT7_API_KEY` environment variable in shell config
3. Context7 MCP server auto-starts with Claude Code via `.mcp.json`

**Token Economics:**
- Context7 queries consume tokens (retrieval + AI processing)
- But more efficient than:
  - AI hallucinating outdated information (requires correction/rework)
  - User manually looking up and pasting documentation (context switching)
  - Embedding full docs in prompts (massive token waste)

### Known Issues

**Cosmetic stderr Warning:**
- Context7 MCP server writes startup message to stderr
- Claude Code logs this as `[ERROR]` but server works perfectly
- Manifests as "1 MCP server failed" on exit (harmless)
- Documented in CONTRIBUTING.md to avoid confusion

## Consequences

### Positive

1. **Overcomes Training Data Lag**: Access to current Python 3.14+ and Claude Code CLI documentation
2. **Benefits All User Groups**: App developers, adapter developers, core maintainers, and plugin developers
3. **Seamless Workflow**: Documentation lookup happens in-context, no browser switching
4. **Always Current**: Documentation updates don't require plugin releases
5. **Version-Specific**: Can access docs for specific Python/library versions
6. **Token-Efficient**: Retrieves relevant excerpts, not entire documentation pages
7. **Multi-Source**: Single MCP server handles both Python and Claude Code docs

### Negative

1. **External Dependency**: Requires Context7 service availability
2. **API Key Required**: Contributors must sign up and configure key (friction in setup)
3. **Network Dependency**: Offline development loses documentation access
4. **Token Cost**: Documentation queries consume Claude API tokens
5. **Service Risk**: Dependent on Context7 service continuity and pricing
6. **stderr Noise**: Cosmetic error message on exit (documented, harmless)

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

- [CLAUDE.md - Documentation Access](../../CLAUDE.md#ai-native-implementation)
- [CONTRIBUTING.md - Context7 Setup](../../CONTRIBUTING.md#2-configure-context7-api-key)
- [.mcp.json - Configuration](../../.mcp.json)
- [Context7 MCP Server](https://github.com/upstash/context7-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ADR-0002: Create Claude Code CLI Plugin](adr-0002-create-claude-code-cli-plugin-for-taew-development.md) - Establishes need for up-to-date documentation access
