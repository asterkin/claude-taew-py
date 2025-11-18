# VISION - claude-taew-py Plugin

## Purpose of This Document

This document captures the desired end state of the claude-taew-py plugin to guide development planning and task prioritization. It serves as a lightweight specification for coordinated work between human and AI collaborators.

**Audience**: Plugin developers (maintainers and contributors)
**Companion documents**:
- [TASKS.md](TASKS.md) - Detailed work breakdown
- [CLAUDE.md](CLAUDE.md) - AI assistant instructions
- [README.md](README.md) - User-facing documentation

---

## Mission

Enable rapid, AI-assisted development of taew-py applications and adapters through intelligent scaffolding, validation, and incremental workflow automation.

**Core principle**: Development happens through **sequential, simple prompts** that incrementally build complete systems - not monolithic code generation.

---

## AI-Native Architecture

### The Problem

New libraries face a vicious cycle in the AI agent era: they're not in LLM training data, so AI agents don't suggest them, so nobody uses them, so they never get into training data.

### The Solution

This plugin implements AI-native tooling through complementary mechanisms:
- **Skills**: Reusable procedures with architectural context (Sonnet)
- **Slash commands**: User-facing workflow shortcuts
- **Sub-agents**: Boilerplate generation (cost-optimized with Haiku)
- **Scripts**: Validation without AI tokens
- **Documentation Access**: Context7 code execution for up-to-date Python 3.14+ and Claude Code CLI documentation

This makes taew-py discoverable and usable through its own AI affordances, not by waiting for training data inclusion.

### Responsibility Matrix

Each component serves a distinct purpose:

| Component | Purpose | Model | Example |
|-----------|---------|-------|---------|
| CLAUDE.md | Static architecture knowledge | N/A | Core patterns, design principles |
| Skills | Reusable procedures with context | Sonnet | doc-query, adr, add-doc |
| Slash Commands | User-facing workflow shortcuts | Routing | /taew-init, /taew-port |
| Scripts | Validation, verification | Local | update-adr-toc, query, list-sources |
| Sub-agents | Delegated boilerplate tasks | Haiku | Adapter scaffolding (future) |
| Config | Model selection, preferences | N/A | .claude/doc-sources.toml |

**Key principle**: Each layer reduces token waste at the layer above.

### Evolution Path: Language-Specific → Language-Agnostic

**Phase 1 (Now): claude-taew-py**
- Python-specific plugin with concrete capabilities
- Bottom-up approach: deliver reliable, testable value first
- Establish patterns for AI-assisted Ports & Adapters development

**Phase 2 (Future): claude-taew-ts, claude-taew-*...**
- Additional language implementations as demand emerges
- Each maintains same architectural philosophy in different ecosystems
- Cross-language learning and pattern refinement

**Phase 3 (Vision): claude-taew orchestrator**
- Language-agnostic meta-plugin
- AI agent recommends implementation language based on application specs
- Polyglot project generation and coordination
- Specification-first development: focus on "what" not "how"

This follows **Promise Theory** (bottom-up capabilities) and **Meta-system Transition** (abstract only after multiple concrete implementations exist).

---

## Target Users & Use Cases

### 1. Application Developers
Building business solutions with taew-py (e.g., car insurance calculator, inventory system)

**Needs**:
- Quick project scaffolding with working CLI
- Add domain models, ports, workflows incrementally
- Auto-generate CLI commands for workflows
- Integrated testing from day one

### 2. Adapter Developers
Creating 3rd-party technology integrations (e.g., AWS, PostgreSQL, Redis)

**Needs**:
- Adapter-specific project structure
- Configuration module patterns
- Contract tests for port implementations
- Clear path to publish adapter

### 3. Core Library Maintainers
Evolving taew-py itself with new stdlib adapters and features

**Needs**:
- Same scaffolding tools work for core development
- Consistency validation across codebase
- ADR management for architectural decisions

---

## Installation & Setup

### Global Installation
Plugin installs to `~/.claude/plugins/taew/` and is available to all projects:

```bash
# Via Claude CLI (if supported)
claude plugin install asterkin/claude-taew-py

# Or via slash command
/plugin install asterkin/claude-taew-py
```

**Documented in**:
- taew-py README.md "Getting Started"
- claude-taew-py README.md

### Per-Project Configuration
Individual projects configure behavior via natural language instructions in their CLAUDE.md file.

**Examples**:

```markdown
# hello-taew-py

This is a taew-py application project.

**Plugin behavior overrides**:
- ALWAYS create a CLI adapter for each application workflow
- DO NOT require ADRs for this project
- Use pytest-bdd instead of CLI integration tests

## Project Overview
...
```

**Common override patterns** (details TBD):
- CLI adapter generation: `ALWAYS create CLI adapter for workflows` or `NEVER create CLI adapters`
- ADR management: `DO NOT require ADRs` or `ALWAYS create ADRs for architectural decisions`
- Testing strategy: `Use Gherkin/pytest-bdd` or `Use Web UI tests only`
- Quality gates: Custom linting rules, test coverage thresholds
- Scaffolding templates: Provide custom templates in `.claude/templates/`

---

## Prerequisites & Auto-Install

### Required Tools
1. **git** - Version control (needs user.name, user.email configuration)
2. **uv** - Python package manager (installs Python 3.14 automatically)
3. **make** - Build automation
4. **Python 3.14+** - Installed via uv

### Optional Tools (Future)
- **gm** - Git workflow manager (TBD: when issue management tools are integrated)
- GitHub CLI (`gh`) for issue management

### Auto-Install Strategy
**Current**: Automatic installation with simple yes/no confirmation
```
The following tools are required but not found:
  - uv (Python package manager)
  - make (build automation)

Install automatically? [Y/n]: _
```

**Future**: More flexible permission model per tool

**Platform support**: Linux only (for now)

---

## Project Types

### Application Projects (`<name>-taew-py`)

**Example**: `hello-taew-py`, `car-insurance-taew-py`

**Initialization** (exact activation TBD):
```
"Create new taew-py application hello-taew-py. Description: Hello World demo"
```
or
```
/taew new app hello-taew-py "Hello World demo"
```

**Generated structure**:
```
hello-taew-py/
├── pyproject.toml          # Dependencies: taew-py from GitHub
├── Makefile                # Standard targets (test, lint, run, etc.)
├── CLAUDE.md               # AI assistant patterns for this app
├── README.md               # Project overview
├── domain/                 # Pure data types (empty initially)
├── ports/                  # Protocol definitions/interfaces (empty initially)
├── workflows/              # Business logic layer (empty initially)
├── adapters/               # Infrastructure layer (empty initially)
│   ├── cli/                # CLI command adapters (created when workflows added)
│   └── ram/                # In-memory storage (created as needed)
├── configuration.py        # Dependency injection wiring
├── bin/
│   └── say                 # CLI entry point executable (name prompted during init)
└── tests/
    └── test_cli_integration.py  # Initial smoke test
```

**Initial CLI test validates**:
- `--help` contains project description
- `--version` returns correct version

**Uses**: [taew/utils/unittest.py](https://github.com/asterkin/taew-py/blob/main/taew/utils/unittest.py) utility class

**CLI shim example**: [HELLO_TAEW_PY.md](https://github.com/asterkin/taew-py/blob/main/HELLO_TAEW_PY.md)

---

### Adapter Projects (`<technology>-taew-py`)

**Example**: `aws-taew-py`, `postgresql-taew-py`

**Initialization**:
```
"Create new taew-py adapter aws. Description: AWS service integrations"
```
or
```
/taew new adapter aws "AWS service integrations"
```

**Generated structure**:
```
aws-taew-py/
├── pyproject.toml          # Dependencies: taew-py + boto3
├── Makefile                # Standard targets
├── CLAUDE.md               # Adapter development patterns
├── README.md               # Adapter documentation
├── adapters/
│   └── taew/
│       └── aws/
│           ├── for_storing_objects/      # S3 adapter
│           │   ├── s3_adapter.py
│           │   └── for_configuring_adapters.py  # Configure class
│           └── for_sending_messages/     # SQS adapter (example)
│               ├── sqs_adapter.py
│               └── for_configuring_adapters.py
├── utils/                  # Optional utility modules
└── test/
    └── test_adapters/
        └── test_aws/
            ├── test_for_storing_objects/
            └── test_for_sending_messages/
```

**Adapter structure examples**:
- Simple app adapter: [bz-taew-py/adapters/ram/for_storing_rates](https://github.com/asterkin/bz-taew-py/tree/main/adapters/ram/for_storing_rates)
- Core adapter: [taew-py/adapters/cli/for_starting_programs](https://github.com/asterkin/taew-py/tree/main/taew/adapters/cli/for_starting_programs)

**Each adapter folder contains**:
- Port implementation modules (one per port interface)
- `for_configuring_adapters.py` with `Configure` class

---

### Core Library Projects (taew-py itself)

**Use case**: Maintaining taew-py, adding stdlib adapters

**Difference from apps/adapters**: Same tools work, but:
- No project initialization (already exists)
- ADR management enabled by default
- Stricter quality gates
- Documentation generation

---

## Development Workflows

### The Sequential Prompt Model

**Philosophy**: Complete systems emerge from incremental, validated steps - not monolithic generation.

**Example flow** - Building car insurance app:

#### Planning Phase
```
User: "Build me a car insurance rate calculator"

Claude: I'll break this down into steps:
  [TodoWrite with sequential prompts]
  1. Create new taew-py application car-insurance
  2. Add domain model Driver (name, age, license_years)
  3. Add domain model Car (model, year, value)
  4. Add port for_calculating_rates
  5. Add RAM adapter for for_calculating_rates
  6. Add workflow for_drivers.request_quote
  7. Add CLI command 'quote' (auto-generated from workflow)
  8. Run tests

User: [Reviews, approves, or modifies plan]
```

#### Execution Phase
Each prompt activates appropriate plugin tooling:

**Prompt 1**: "Create new taew-py application car-insurance. Description: Car insurance rate calculator"
- Validates prerequisites (git, uv, make, Python 3.14)
- Scaffolds project structure
- Generates initial CLI + integration test
- Validates: tests pass, lint passes

**Prompt 2**: "Add domain model Driver with fields: name (str), age (int), license_years (int)"
- Creates `src/car_insurance/domain/driver.py`
- Adds type hints, validation, comparison methods
- Updates imports
- Validates: type checking passes

**Prompt 3-4**: Similar for Car model and port interface

**Prompt 5**: "Add RAM adapter for for_calculating_rates with simple age-based formula"
- Creates `adapters/ram/for_calculating_rates/` folder
- Generates adapter implementation + Configure class
- Creates integration test
- Validates: adapter tests pass

**Prompt 6**: "Add workflow for_drivers.request_quote using for_calculating_rates port"
- Creates `workflows/for_drivers/request_quote.py`
- Auto-wires port dependency
- Example: [bz-taew-py/workflows/for_car_drivers](https://github.com/asterkin/bz-taew-py/tree/main/workflows/for_car_drivers)

**Prompt 7**: Auto-triggered by workflow creation (if `auto_cli_for_workflows = true`)
- Creates CLI adapter in `adapters/cli/for_drivers/`
- Maps workflow to CLI command
- Example: [bz-taew-py/adapters/cli](https://github.com/asterkin/bz-taew-py/tree/main/adapters/cli)
- Updates CLI shim to register command

**Prompt 8**: "Run tests"
- Executes: `make test`
- Reports results

### Key Plugin Capabilities (TBD: Skills vs Other Tools)

**To be designed**:
- TODO list generation from high-level descriptions
- Prompt routing (detect "Add port..." → invoke scaffolding)
- Incremental validation (after each step)
- Smart dependency resolution ("add aws adapters" → GitHub reference)

**Naming convention resolution**:
```
Prompt: "add aws adapters"
Plugin: Adds to pyproject.toml:
  aws-taew-py = { git = "https://github.com/asterkin/aws-taew-py" }
```

---

## Quality & Testing Strategy

### Automatic Quality Gates

**After each scaffolding operation**:
1. **Type checking**: pyright (Pylance strict mode in VSCode)
2. **Linting**: ruff
3. **Tests**: unittest (generated + existing)
4. **Build**: make build (validates all imports)

**Tools**:
- make
- ruff
- pyright (from Pylance/VSCode - default IDE)
- unittest (Python stdlib)

### Testing Levels

#### 1. CLI Integration Tests (Applications)
**Generated automatically** for new apps and workflows

**Uses**: `taew.utils.unittest.py`

**Validates**:
- Help text contains description
- Version command returns correct version
- Workflow commands execute successfully

#### 2. Adapter Integration Tests
**Generated per adapter** (RAM, CLI, 3rd-party)

**Validates**:
- Port interface contract compliance
- Configuration loading
- Happy path execution

**Note**: Full integration (Docker, real services) is optional per project

#### 3. Unit Tests (Optional)
**For complex domain logic or adapter internals**

**Not auto-generated** - developer decides when needed

### ADR Management

**Default**: Enabled for all projects (can be disabled per-project in CLAUDE.md)

**Triggers**:
- Adopting new tool or technology
- Architectural pattern decisions
- Testing strategy changes

**Tooling**: Existing `adr` skill (already implemented)

---

## Dependency Management

### taew-py Core Dependency
All projects add taew-py from GitHub:

```toml
[project]
dependencies = [
    "taew-py @ git+https://github.com/asterkin/taew-py.git"
]
```

### 3rd-Party Adapter Dependencies (Applications)
Naming convention-based resolution:

**Prompt**: "add postgresql adapters"

**Generated**:
```toml
[project]
dependencies = [
    "taew-py @ git+https://github.com/asterkin/taew-py.git",
    "postgresql-taew-py @ git+https://github.com/asterkin/postgresql-taew-py.git"
]
```

**Future**: Support PyPI packages when adapters are published

### Technology SDK Dependencies (Adapters)
Plugin prompts for or infers required SDKs:

**Example** - PostgreSQL adapter:
```toml
[project]
dependencies = [
    "taew-py @ git+https://github.com/asterkin/taew-py.git",
    "psycopg[binary]>=3.2"
]
```

---

## Future Enhancements

### 1. Gherkin-Style Acceptance Testing
**Vision**: taew-flavored Cucumber with pure Python step definitions

**Example**: [bz-taew/docs/features](https://github.com/asterkin/bz-taew/tree/main/docs/features)

**Key differentiator**:
- Steps are Python classes/functions
- Auto-wired with adapters via configuration
- No magic strings or regex matching

**Inspired by**: cucumber.js implementation (previous work)

**Tooling**:
- Generate feature files from use case descriptions
- Generate step definition skeletons (pure Python classes/functions)
- Auto-wire steps to ports/adapters via configuration
- Run via unittest-based test runner (not pytest)

**Status**: Future project, not v1.0 scope

### 2. Issue Management Integration
**Tools**: `gh` (GitHub CLI), potentially `gm`

**Workflows**:
- Create issue → create branch → link them
- PR creation with auto-generated descriptions
- Issue/PR status synchronization

**Decision**: TBD whether slash commands or skills

**Prerequisites**: Add `gh` and `gm` to auto-install, documentation sources

### 3. Web UI Scaffolding
**For applications** that need web interfaces instead of/in addition to CLI

**Overrides**: `cli_adapter = false` in project config

**Not v1.0 scope**

### 4. Adapter Publication Workflow
**For adapter developers** ready to share work

**Features**:
- PyPI publishing automation
- Version bump + changelog generation
- Submit adapter to taew-py core (PR creation)

**Decision**: TBD timing and priority

**Note**: Multi-language support strategy is covered in [AI-Native Architecture](#ai-native-architecture) section.

---

## Open Questions & TBD Items

### High Priority (Affects Initial Implementation)

1. **Init command activation**:
   - Natural language: "Create new taew-py application..."
   - Slash command: `/taew new app ...`
   - Hybrid: Both with smart routing

2. **TODO list tooling**:
   - How to generate task list from high-level descriptions?
   - How to route prompts to appropriate scaffolding tools?
   - Integration with existing TodoWrite?

3. **Skill vs other tool boundaries**:
   - What should be skills (Sonnet)?
   - What should be sub-agents (Haiku)?
   - What should be scripts (no tokens)?

4. **AI assistant integration files**:
   - Generate AGENTS.md for project context
   - Configuration files for GitHub Copilot VSCode plugin
   - Configuration files for Codex integration
   - Details TBD: What metadata to include, update frequency, format

5. **Project overrides mechanism**:
   - Just CLAUDE.md with documented conventions?
   - `.claude/taew-overrides.toml`?
   - Both?

### Medium Priority (Can Decide During Development)

5. **Auto-install permission granularity**:
   - All-or-nothing confirmation?
   - Per-tool prompts?
   - Remember decision per project?

6. **Adapter testing strategy**:
   - Always contract tests only?
   - Optional Docker/testcontainers integration?
   - Let developer decide per adapter?

7. **Issue management default**:
   - Auto-install `gh` + `gm`?
   - Opt-in only?
   - Part of v1.0 or later?

### Low Priority (Nice to Have)

8. **Plugin update mechanism**:
   - User runs `git pull` in `~/.claude/plugins/taew/`?
   - Claude CLI auto-update?
   - Version checking?

9. **Tutorial execution automation**:
   - Can HELLO_TAEW_PY.md be executed as scripted prompts?
   - Validation that tutorial still works?

10. **Cross-project coordination**:
    - Working on app + custom adapter simultaneously?
    - Local development links between projects?

---

## Success Metrics

### Quantitative
- **Time to scaffold new app**: < 2 minutes (from init prompt to passing tests)
- **Time to add port + adapter**: < 5 minutes
- **Generated code quality**: 100% pass type checking + linting
- **Test coverage**: CLI tests auto-generated for 100% of workflows

### Qualitative
- Developer can build complete MEP without reading taew-py source code
- Tutorial (HELLO_TAEW_PY.md) executable as sequential prompts
- Plugin works equally well for apps, adapters, and core maintenance
- Generated code feels hand-written, not templated

### Adoption
- Used for all new taew-py applications
- Used for at least 3 published 3rd-party adapters
- Contributes to taew-py core development productivity

---

## Next Steps

1. **Review & refine this vision** - Ensure alignment on end state
2. **Create TASKS.md** - Break down into concrete, prioritized work items
3. **Decide TBD items** - Make architectural decisions (via ADRs where appropriate)
4. **Implement v1.0 scope** - Focus on application scaffolding + quality gates
5. **Iterate based on usage** - Refine based on real development experience

---

## Appendix: Initial Planning Options

These were the initial candidates considered during the vision planning session (2025-11-17):

### 1. Import Issue Slash Commands
**Source**: https://github.com/asterkin/taew-py/tree/main/.claude/commands

**Rationale**: Coordinated issue/branch management workflow automation

**Questions**:
- Slash commands vs skills (more flexible)?
- Which ADR to produce?
- Add git and gh documentation to doc-sources.toml?

**Status**: Deferred until concrete workflow pain point emerges

---

### 2. Add Quality Tooling (make, ruff, mypy, pyright)
**Rationale**: Automation of custom scripts quality checks

**Questions**:
- ADR for toolchain selection?
- Hook integration (pre-commit vs custom hooks)?
- Scope: plugin scripts only, generated code, or both?

**Status**: High priority - decided to use ruff + pyright (from Pylance/VSCode)

---

### 3. Coverage and Unit Tests for Custom Scripts
**Rationale**: Quality assurance for plugin infrastructure

**Questions**:
- ADR for testing strategy?
- What to test (deterministic scripts vs LLM outputs)?
- When to test (pre-commit, CI, manual)?

**Status**: Deferred until tooling (#2) stabilizes and more scripts exist

---

### 4. Produce First Plugin Version
**Rationale**: Make existing work (ADRs, doc-query, add-doc skills) usable and documented

**Scope**:
- Working skills ✅
- Documentation ✅
- Quick start guide ⚠️
- Versioning/changelog ⚠️

**Status**: Highest priority - this VISION.md addresses documentation gap

---

### 5. Add `uv` to Tool List
**Rationale**: Modern Python packaging standard, fits all use cases (apps, adapters, core)

**Action**: Add to doc-sources.toml via add-doc skill

**Status**: Quick win - should be done alongside #4

---

### 6. Analyze HELLO_TAEW_PY.md for Scaffolding Requirements
**Source**: https://github.com/asterkin/taew-py/blob/main/HELLO_TAEW_PY.md

**Rationale**: Core plugin functionality - teaching Claude how to build taew apps

**Phased approach**:
1. **Phase 1 (now)**: Extract patterns, create ADR for scaffolding strategy
2. **Phase 2 (post-v0.1.0)**: Implement critical skills (`/taew-init`, `/taew-port`)
3. **Phase 3**: Complete scaffolding suite

**Status**: High priority, but phased - start with exploratory analysis

---

### 7. Extend Plugin for 3rd-Party Adapters
**Rationale**: Support adapter ecosystem development

**Dependencies**: Requires #6 (core scaffolding) working first

**Scope questions**:
- Skills to scaffold adapters?
- Example adapters as templates?
- Adapter development guide?

**Status**: Deferred until #6 Phase 2 complete - natural progression from apps to adapters

---

### Prioritization Summary (From Planning Session)

**Immediate** (Week 1):
1. ✅ Package v0.1.0 - ADR & Documentation Access (VISION.md created)
2. ⏭️ Add `uv` via add-doc skill

**Next Sprint**:
3. 📋 #6 Phase 1: Analyze HELLO_TAEW_PY.md, extract patterns, create ADR
4. 🔧 #2: Add ruff/pyright tooling with ADR

**Future**:
5. 🧪 #3: Testing infrastructure
6. 🏗️ #6 Phase 2: Implement core scaffolding skills
7. 🔌 #7: 3rd-party adapter support
8. 🌊 #1: Git workflow integration (only if needed)

---

**Document status**: Living specification
**Last updated**: 2025-11-17
**Owner**: claude-taew-py maintainers
