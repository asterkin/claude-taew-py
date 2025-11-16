# claude-taew-py

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-blue.svg)](https://code.claude.com/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-CLI-5A67D8.svg)](https://code.claude.com/)

Claude Code CLI plugin for AI-assisted development with taew-py Ports & Adapters foundation library.

## Who Is This For?

This plugin is designed for:
- **Application developers** building software with taew-py
- **Adapter developers** creating 3rd-party technology integrations
- **Core maintainers** contributing to taew-py itself

## Why AI-Native?

### The Problem

New libraries face a vicious cycle in the AI agent era: they're not in LLM training data, so AI agents don't suggest them, so nobody uses them, so they never get into training data.

### The Solution

Ship AI-native tooling alongside the library itself:
- **Skills**: Reusable procedures with architectural context
- **Slash commands**: User-facing workflow shortcuts
- **Sub-agents**: Cost-optimized boilerplate generation
- **Scripts**: Validation without burning AI tokens

This makes taew-py discoverable and usable through its own AI affordances, not by waiting for training data inclusion.

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

## Core Philosophy

Understanding taew-py's architectural principles:

- **taew-py core**: Stays at Python stdlib level (language extension)
- **3rd-party adapters**: Separate projects (AWS, GCP, PostgreSQL, etc.)
- **Dynamic-first**: Dynamic wiring by default, static as deployment optimization
- **CLI-first**: Easiest path to explore workflows, then extend to TUI/Web/etc.

## Contributing

Interested in contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions, including how to configure the required Context7 API key for accessing up-to-date Python 3.14+ and Claude Code CLI documentation.

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
