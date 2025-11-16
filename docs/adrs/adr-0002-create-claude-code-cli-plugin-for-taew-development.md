# ADR-0002: Create Claude Code CLI Plugin for taew Development

**Status:** Accepted

## Context

### The Library Adoption Challenge in the AI Era

**taew-py** is a Python 3.14+ foundation library that makes Ports & Adapters (Hexagonal Architecture) natural and fast, enabling rapid development of Minimal Evolvable Products (MEPs) for early-stage startups. However, new libraries face a fundamental challenge in the era of AI-assisted development:

**The Vicious Cycle:**
1. New libraries aren't in LLM training data
2. AI agents don't suggest them to developers
3. Developers don't discover or adopt them
4. Libraries remain absent from future training data
5. Cycle repeats

This creates a chicken-and-egg problem: libraries need adoption to get into training data, but need to be in training data to get adoption when developers increasingly rely on AI coding assistants.

### Traditional Solutions Are Insufficient

**Traditional approaches to library adoption:**
- Documentation websites (developers must find them first)
- Package registries (requires knowing library exists)
- Tutorials and examples (assumes awareness)
- Community evangelism (slow, doesn't scale)
- Waiting for training data inclusion (passive, uncertain timeline)

**None of these solve the core problem**: AI agents recommending libraries they weren't trained on.

### AI-Native Opportunity

Claude Code CLI and similar AI coding assistants support extensibility through:
- **Skills**: Reusable procedures with architectural context
- **Slash commands**: User-facing workflow shortcuts
- **MCP servers**: Real-time data and tool access
- **Project context**: CLAUDE.md files for static knowledge

This creates an opportunity: **ship AI-native tooling alongside the library itself**, making the library discoverable and usable through AI affordances rather than waiting for passive training data inclusion.

### Three User Archetypes

The taew-py ecosystem has three distinct user groups with different needs:

1. **Application Developers**: Building products with taew-py
   - Need: Scaffolding projects, creating domain models, ports, workflows, adapters
   - Challenge: Learning Ports & Adapters patterns while staying productive

2. **3rd-Party Adapter Developers**: Creating technology integrations (AWS, GCP, PostgreSQL, etc.)
   - Need: Following taew-py adapter patterns and conventions
   - Challenge: Maintaining consistency across external adapter projects

3. **Core Library Maintainers**: Contributing to taew-py itself
   - Need: Adding stdlib adapters, maintaining patterns
   - Challenge: Ensuring all tooling works equally across contexts

**Implication**: A single plugin must support all three contexts with reusable workflows.

### Strategic Background

Detailed exploration of this challenge and potential solutions documented in:
- [Claude Web Strategy Conversation](../strategy/claude-web.pdf)
- [ChatGPT Web Strategy Conversation](../strategy/chatgpt-web.pdf)

Key insights from these conversations:
- AI-native tooling breaks the adoption cycle by embedding library knowledge directly into AI tools
- Bottom-up approach (concrete implementation first, abstraction later) reduces risk
- Phased evolution (Python-specific → multi-language → language-agnostic) provides learning path
- Meta-level consistency (plugin mirrors library's architectural philosophy) improves coherence

## Decision

Create **claude-taew-py**, a Claude Code CLI plugin that teaches Claude Code how to scaffold and develop taew-py applications, 3rd-party adapters, and core library features.

### Core Capabilities

The plugin provides:

1. **Skills**: Reusable procedures with architectural context (Sonnet-level reasoning)
   - Port creation following hexagonal patterns
   - Adapter scaffolding with proper contracts
   - Workflow composition guidance
   - Domain model design assistance

2. **Slash Commands**: User-facing workflow shortcuts
   - `/taew-init`: Scaffold new projects
   - `/taew-port`: Create ports with templates
   - `/taew-adapter`: Generate adapter skeletons
   - Additional commands as patterns emerge

3. **Sub-Agents**: Cost-optimized boilerplate generation (Haiku)
   - Delegated tasks for repetitive code generation
   - Adapter boilerplate from technology specifications
   - Test scaffolding following project patterns

4. **Scripts**: Validation without AI tokens
   - Type checking and linting
   - Architecture pattern validation
   - Dependency analysis
   - Test execution

5. **Documentation Access**: Context7 MCP integration
   - Real-time Python 3.14+ documentation lookup
   - Claude Code CLI best practices access
   - Overcomes training data lag for rapidly evolving technologies

### Responsibility Matrix

Each component has a specific role to reduce token waste:

| Component | Purpose | Model | Example |
|-----------|---------|-------|---------|
| CLAUDE.md | Static architecture knowledge | N/A | Core patterns, design principles |
| Skills | Reusable procedures with context | Sonnet | "Create port following pattern" |
| Slash Commands | User-facing workflow shortcuts | Routing | /taew-init, /taew-port |
| Scripts | Validation, verification | Local | make test, type checking |
| Sub-agents | Delegated boilerplate tasks | Haiku | Generate adapter scaffolding |

**Key Principle**: Each layer reduces token waste at the layer above.

### Evolution Path: Bottom-Up Abstraction

**Phase 1 (Now): claude-taew-py**
- Python-specific plugin with concrete capabilities
- Bottom-up approach: deliver reliable, testable value first
- Establish patterns for AI-assisted Ports & Adapters development
- Support all three user archetypes (app, adapter, core)

**Phase 2 (Future): claude-taew-ts, claude-taew-*...**
- Additional language implementations as demand emerges
- Each maintains same architectural philosophy in different ecosystems
- Cross-language learning and pattern refinement
- Only after Python implementation proves value

**Phase 3 (Vision): claude-taew orchestrator**
- Language-agnostic meta-plugin (only after multiple concrete implementations)
- AI agent recommends implementation language based on application specs
- Polyglot project generation and coordination
- Specification-first development: focus on "what" not "how"

**Rationale for Phased Approach**:
- Follows **Promise Theory**: Build bottom-up capabilities, not top-down mandates
- Follows **Meta-system Transition**: Abstract only after multiple concrete implementations exist
- Reduces risk: Validate approach with one language before expanding
- Enables learning: Each implementation informs architectural refinement

### Meta-Level Consistency

The plugin mirrors taew-py's philosophy at the meta-level:
- **Core patterns are technology-neutral**: Skills focus on architectural concepts, not implementation details
- **Implementation details are adapters**: Language-specific code generation is "adapted" to each context
- **Claude integration itself is "just another adapter layer"**: The plugin follows the same decoupling principles it teaches

This consistency helps users internalize Ports & Adapters thinking while using the tool.

## Consequences

### Positive

1. **Breaks Adoption Cycle**: Library becomes discoverable through AI affordances, not training data
2. **Immediate Value**: Developers get productivity benefits from day one
3. **Consistent Patterns**: AI guidance ensures proper architectural patterns across all three user contexts
4. **Scales Automatically**: As AI assistants improve, the plugin's value increases
5. **Learning Mechanism**: Using the tool teaches Ports & Adapters principles
6. **Future-Proof**: Plugin evolution path supports multi-language and specification-first development
7. **Token Efficiency**: Layered approach (Skills/Scripts/Sub-agents) optimizes AI usage costs

### Negative

1. **Plugin Maintenance**: Additional codebase to maintain alongside core library
2. **Version Synchronization**: Plugin must stay synchronized with library evolution
3. **Learning Curve**: Contributors need to understand both taew-py AND Claude Code plugin development
4. **Claude Code Dependency**: Tied to Anthropic's ecosystem and CLI evolution
5. **Fragmentation Risk**: Supporting multiple user archetypes could lead to complexity
6. **Premature Abstraction Risk**: Phase 2/3 evolution might not materialize or might need different approach

### Neutral

1. **Meta-Complexity**: Plugin that teaches architecture must itself follow good architecture
2. **Documentation Dual Role**: Content serves both humans and AI agents
3. **Bootstrapping Challenge**: Initial plugin development happens without the plugin (resolved by ADR-0001 tooling)
4. **Community Building**: Plugin becomes shared infrastructure requiring collaboration
5. **Multi-Language Future**: Evolution to Phase 2/3 depends on Phase 1 success and demand

## Alternatives Considered

### 1. Wait for Training Data Inclusion
**Rejected**: Passive approach with uncertain timeline, doesn't solve discovery problem

### 2. Traditional Documentation Only
**Rejected**: Doesn't help AI agents recommend the library; developers still need to discover it first

### 3. Generic AI Assistant (Not Claude Code Specific)
**Rejected**: Less integration with developer workflow; skill/command system provides better UX

### 4. Start with Language-Agnostic Plugin
**Rejected**: Violates bottom-up principle; high risk without concrete validation

### 5. Separate Plugins Per User Archetype
**Rejected**: Creates fragmentation; reusable workflows better serve all three groups

## References

- [README.md - "Why AI-Native?"](../../README.md#why-ai-native)
- [README.md - Evolution Path](../../README.md#evolution-path-language-specific--language-agnostic)
- [CLAUDE.md - Responsibility Matrix](../../CLAUDE.md#responsibility-matrix)
- [ADR-0001: Use AI-Assisted Tooling for ADR Creation](adr-0001-use-ai-assisted-tooling-for-adr-creation.md) (demonstrates the plugin's meta-level approach)
- [Claude Web Strategy Conversation](../strategy/claude-web.pdf)
- [ChatGPT Web Strategy Conversation](../strategy/chatgpt-web.pdf)
- [taew-py Core Library](https://github.com/asterkin/taew-py)
