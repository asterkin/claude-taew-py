# Contributing to claude-taew-py

Thank you for your interest in contributing to claude-taew-py! This guide will help you get started.

## Documentation Guide

This project uses a structured documentation architecture to support AI-assisted development:

- **[VISION.md](VISION.md)** - Project philosophy, strategic goals, and long-term roadmap
- **[docs/adrs/README.md](docs/adrs/README.md)** - Architecture Decision Records catalog, including all coding and style guidelines
- **[CLAUDE.md](CLAUDE.md)** - Operational instructions that Claude Code CLI follows automatically during AI-assisted development sessions (tool activation, coding standards reminders, development workflow)

## Prerequisites

Before you begin, ensure you have:

1. **Git** - For cloning the repository and version control
2. **Python 3.12+** - Required for development tooling (ADR scripts, validation, etc.)
   ```bash
   python3 --version  # Should show 3.12.x or higher
   ```
   **Note**: While this plugin targets Python 3.14+ for taew-py application development, the development scripts require Python 3.12+ (widely available). Later, these scripts may be rewritten using taew-py itself.

3. **Context7 API Key** - For accessing up-to-date Python 3.14+ and Claude Code CLI documentation

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/asterkin/claude-taew-py.git
cd claude-taew-py
```

### 2. Configure Context7 API Key

This plugin uses the Context7 MCP server to access up-to-date documentation for Python 3.14+ and Claude Code CLI. You'll need to configure your Context7 API key:

#### Get Your API Key

1. Visit [Context7](https://context7.com)
2. Sign up or log in to your account
3. Navigate to your API settings
4. Copy your API key

#### Set the Environment Variable

Add the following to your shell configuration file (`~/.bashrc`, `~/.zshrc`, or equivalent):

```bash
export CONTEXT7_API_KEY="your-api-key-here"
```

Then reload your shell configuration:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

#### Verify Configuration

Test the doc-query skill with natural questions that trigger documentation lookup:

**Example prompts to try:**
- "How do I write Python async generators?"
- "How do I define Claude Code skills?"
- "What's the syntax for Python 3.14 pattern matching?"

The doc-query skill will automatically activate and fetch current documentation from Context7.

### 3. Install Dependencies

Currently no external dependencies are required - all code uses Python 3.12+ stdlib only (urllib for HTTP requests, etc.).

The `requirements.txt` file is kept for future dependencies as the project evolves.

## Development Workflow

### Project Structure

This project follows the self-contained skills pattern and strict documentation boundaries. See [ADR-0004: Project Structure and Documentation Standards](docs/adrs/adr-0004-project-structure-and-documentation-standards.md) for:

- Skills organization and encapsulation principles
- Documentation file responsibilities and token budgets
- Code structure patterns (utilities, templates, scripts)
- Cross-reference conventions

**Quick reference**:
```
claude-taew-py/
├── .claude/             # Claude Code tools and configurations
│   └── skills/          # Self-contained skills (scripts + templates)
├── docs/adrs/           # Architecture Decision Records
├── CLAUDE.md            # AI operational directives (token-optimized)
├── VISION.md            # Strategic goals and philosophy
├── CONTRIBUTING.md      # This file
└── README.md            # Entry point for end users
```

### Making Changes

1. Create a feature branch from `main`
2. Make your changes following the project's architecture principles (see [CLAUDE.md](CLAUDE.md) and [ADRs](docs/adrs/))
3. Document significant architectural decisions (create ADRs using `/adr` or `doc-query` skill)
4. Test your changes with Claude Code
5. Submit a pull request

### Testing Skills and Commands

When developing skills or slash commands:
- Test them in a real taew-py project context
- Verify they work for all three use cases (app development, adapter development, core maintenance)
- Ensure generated code follows taew-py architectural patterns

## Questions or Issues?

If you encounter any problems or have questions:

1. **For tool documentation** (Python 3.14+, Claude Code CLI):
   - Use the **doc-query skill** for up-to-date documentation
   - Example: "How do I use Python 3.14 type parameter syntax?"
   - See [ADR-0003](docs/adrs/adr-0003-use-context7-mcp-for-documentation-access.md) for rationale

2. **For project issues**:
   - Check existing [GitHub Issues](https://github.com/asterkin/claude-taew-py/issues)
   - Open a new issue with details about your setup and the problem

3. **For architectural decisions**:
   - Review [Architecture Decision Records](docs/adrs/README.md)
   - Create new ADRs using the adr skill for significant changes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
