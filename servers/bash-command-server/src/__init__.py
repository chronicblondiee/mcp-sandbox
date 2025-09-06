"""
FastMCP 2.0 Bash Command Server

A secure MCP server that allows execution of bash commands with proper
safety measures and error handling.
"""

from .bash_command_server import mcp, execute_bash_command

__version__ = "1.0.0"
__all__ = ["mcp", "execute_bash_command"]