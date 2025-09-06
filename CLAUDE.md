# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a sandbox repository for developing Model Context Protocol (MCP) servers. The repository uses Python with uv for package management and is configured specifically for MCP 2.0 server development.

## Development Environment

- **Python Package Manager**: uv (modern Python package manager)
- **Target Framework**: MCP 2.0 for building context protocol servers
- **License**: MIT License

## Key Tools and Commands

Since this is a sandbox repository without existing Python projects, commands will depend on the specific MCP server being developed. Common patterns for MCP development with uv:

```bash
# Initialize new MCP server project
uv init --lib <server-name>

# Install MCP dependencies
uv add mcp

# Run MCP server (typical pattern)
uv run python -m <server-module>

# Install development dependencies
uv add --dev pytest ruff mypy

# Run tests (when implemented)
uv run pytest

# Code formatting and linting
uv run ruff check
uv run ruff format
uv run mypy .
```

## Architecture Guidelines

### MCP Server Structure
- Use `mcp.server.Server` class for MCP 2.0 compliance
- Implement proper async/await patterns for MCP operations
- Structure projects with `pyproject.toml` for uv compatibility
- Follow JSON-RPC message handling standards
- Include comprehensive error handling and input validation

### Project Organization
- Each MCP server should have its own directory structure
- Use proper Python package structure with `__init__.py` files
- Include proper logging and error responses
- Implement tools, resources, and prompts according to MCP 2.0 specs

## Claude Code Agent Configuration

The repository includes a specialized agent for MCP server development:
- **Agent**: `mcp-server-builder` (located in `.claude/agents/`)
- **Purpose**: Expert assistance for MCP 2.0 server development using Python and uv
- **Capabilities**: Server design, implementation, debugging, and testing

## Development Notes

- This is a sandbox environment for experimentation with MCP servers
- The repository structure is minimal by design to allow flexible project creation
- All MCP server projects should use uv for dependency management
- Focus on MCP 2.0 specification compliance for any server implementations