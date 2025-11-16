# Contributing to claude-taew-py

Thank you for your interest in contributing to claude-taew-py! This guide will help you get started.

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

You can verify that the Context7 integration is working by starting Claude Code in this project directory and asking it to confirm access to Python 3.14 and Claude Code CLI documentation.

**Known Issue**: You may see `"1 MCP server failed"` when exiting Claude Code. This is harmless - the Context7 MCP server writes startup messages to stderr, which Claude Code logs as an error. The server works perfectly (verify with `/mcp` command). This is a cosmetic issue that doesn't affect functionality.

### 3. Prerequisites

**Python 3.12 or higher** is required for development tooling (scripts for ADR management, validation, etc.).

Verify your Python version:
```bash
python3 --version  # Should show 3.12.x or higher
```

**Note**: While this plugin targets Python 3.14+ for application development with taew-py, the development scripts require Python 3.12+ (widely available on most systems). Later, these scripts may be rewritten using taew-py itself with uv for better integration.

### 4. Install Dependencies

```bash
# Add any project-specific setup steps here as the project evolves
```

## Development Workflow

### Project Structure

```
claude-taew-py/
├── .claude/
│   ├── commands/        # Slash commands
│   └── skills/          # Skills
├── scripts/             # Validation scripts
├── CLAUDE.md           # AI context and architecture
├── README.md           # Project overview
└── CONTRIBUTING.md     # This file
```

### Making Changes

1. Create a feature branch from `main`
2. Make your changes following the project's architecture principles (see CLAUDE.md)
3. Test your changes with Claude Code
4. Submit a pull request

### Testing Skills and Commands

When developing skills or slash commands:
- Test them in a real taew-py project context
- Verify they work for all three use cases (app development, adapter development, core maintenance)
- Ensure generated code follows taew-py architectural patterns

## Questions or Issues?

If you encounter any problems or have questions:
- Check existing [GitHub Issues](https://github.com/asterkin/claude-taew-py/issues)
- Open a new issue with details about your setup and the problem
- For Claude Code CLI issues, see the [official documentation](https://code.claude.com/docs)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
