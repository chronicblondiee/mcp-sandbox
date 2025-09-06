# FastMCP 2.0 Bash Command Server

A secure MCP server that allows execution of bash commands with comprehensive safety measures and error handling.

## Features

- **HTTP transport** - Web-accessible MCP server (default on port 8000)
- **Security-first design** with command filtering, timeouts, and validation
- **FastMCP 2.0 compliant** with proper async/await implementation
- **Three MCP tools**: `execute_bash`, `list_safe_commands`, `get_security_info`
- **Comprehensive error handling** and logging
- **Working directory support** with validation
- **Flexible transport** - Supports both HTTP and stdio transports

## Security Features

- Command length limits (1000 characters max)
- Blocked dangerous commands (`rm`, `sudo`, `shutdown`, etc.)
- Pattern-based filtering (pipes, redirects, command injection)
- 30-second execution timeout
- Limited environment variables for security
- Input sanitization and validation

## Quick Start

### HTTP Transport (Default)

```bash
# Start the server with HTTP transport on default port 8000
./start_server.sh

# Or with custom port
./start_server.sh --port 9000

# Or manually
uv run python src/bash_command_server.py --port 8000 --transport http

# Server will be available at: http://127.0.0.1:8000/mcp
```

### Stdio Transport (Legacy)

```bash
# Start with stdio transport
./start_server.sh --transport stdio

# Or manually
uv run python src/bash_command_server.py --transport stdio
```

## Testing

```bash
# Run the test suite
uv run python tests/test_server.py

# Run usage examples
uv run python examples/example_usage.py
```

## Directory Structure

```
bash-command-server/
├── src/
│   ├── __init__.py
│   └── bash_command_server.py    # Main server implementation
├── tests/
│   └── test_server.py           # Test suite
├── examples/
│   └── example_usage.py         # Usage demonstrations
├── server_config.json           # Server configuration
├── start_server.sh             # Startup script
└── README.md                   # This file
```

## MCP Tools

### execute_bash
Execute bash commands safely with security restrictions.

**Parameters:**
- `command` (str): The bash command to execute (max 1000 characters)
- `working_directory` (str, optional): Directory to run the command in

**Returns:**
- `success` (bool): Whether the command succeeded
- `stdout` (str): Standard output from the command
- `stderr` (str): Standard error from the command
- `return_code` (int): Exit code of the command
- `command` (str): The executed command
- `working_dir` (str): The directory where command was executed
- `error` (str): Error message if command failed or was blocked

### list_safe_commands
Get a list of commonly used safe commands that can be executed.

### get_security_info
Get information about the security measures in place for bash command execution.

## Development

This server uses FastMCP 2.0 framework with uv for package management. The implementation follows MCP 2.0 specifications with proper tool decorators and async patterns.

## License

MIT License