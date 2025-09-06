#!/usr/bin/env python3
"""
FastMCP 2.0 Bash Command Execution Server

A secure MCP server that allows execution of bash commands with proper
safety measures and error handling.
"""

import asyncio
import logging
import subprocess
import shlex
from typing import Any, Dict, List, Optional
import os
from pathlib import Path

from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security configuration
MAX_COMMAND_LENGTH = 1000
TIMEOUT_SECONDS = 30
BLOCKED_COMMANDS = {
    'rm', 'rmdir', 'del', 'format', 'fdisk', 'mkfs',
    'dd', 'shutdown', 'reboot', 'halt', 'poweroff',
    'sudo', 'su', 'passwd', 'chown', 'chmod',
    'crontab', 'at', 'batch', 'systemctl', 'service'
}
BLOCKED_PATTERNS = [
    '&&', '||', ';', '|', '>', '>>', '<', '`', '$(',
    'eval', 'exec', 'source', '.', 'wget', 'curl -X'
]

def is_command_safe(command: str) -> tuple[bool, str]:
    """
    Check if a command is safe to execute.
    
    Returns:
        tuple: (is_safe, reason_if_unsafe)
    """
    if len(command) > MAX_COMMAND_LENGTH:
        return False, f"Command too long (max {MAX_COMMAND_LENGTH} characters)"
    
    # Check for blocked commands
    parts = shlex.split(command.lower())
    if parts and parts[0] in BLOCKED_COMMANDS:
        return False, f"Blocked command: {parts[0]}"
    
    # Check for blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if pattern in command:
            return False, f"Blocked pattern detected: {pattern}"
    
    # Check for suspicious characters
    if any(char in command for char in ['$(', '`', '{', '}']):
        return False, "Command contains potentially dangerous characters"
    
    return True, ""

async def execute_bash_command(command: str, working_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Safely execute a bash command with timeout and error handling.
    
    Args:
        command: The bash command to execute
        working_dir: Optional working directory for command execution
        
    Returns:
        Dict containing stdout, stderr, return_code, and execution info
    """
    # Validate command safety
    is_safe, reason = is_command_safe(command)
    if not is_safe:
        return {
            "success": False,
            "error": f"Command blocked for security: {reason}",
            "stdout": "",
            "stderr": "",
            "return_code": -1,
            "command": command,
            "working_dir": working_dir or os.getcwd()
        }
    
    # Validate working directory if provided
    if working_dir:
        working_path = Path(working_dir)
        if not working_path.exists():
            return {
                "success": False,
                "error": f"Working directory does not exist: {working_dir}",
                "stdout": "",
                "stderr": "",
                "return_code": -1,
                "command": command,
                "working_dir": working_dir
            }
        if not working_path.is_dir():
            return {
                "success": False,
                "error": f"Working directory path is not a directory: {working_dir}",
                "stdout": "",
                "stderr": "",
                "return_code": -1,
                "command": command,
                "working_dir": working_dir
            }
    
    try:
        logger.info(f"Executing command: {command}")
        if working_dir:
            logger.info(f"Working directory: {working_dir}")
        
        # Execute command with timeout
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_dir,
            # Limit environment for security
            env={
                'PATH': os.environ.get('PATH', ''),
                'HOME': os.environ.get('HOME', ''),
                'USER': os.environ.get('USER', ''),
                'PWD': working_dir or os.getcwd()
            }
        )
        
        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=TIMEOUT_SECONDS
            )
            return_code = process.returncode
        except asyncio.TimeoutError:
            # Kill the process if it times out
            process.kill()
            await process.wait()
            return {
                "success": False,
                "error": f"Command timed out after {TIMEOUT_SECONDS} seconds",
                "stdout": "",
                "stderr": "",
                "return_code": -1,
                "command": command,
                "working_dir": working_dir or os.getcwd()
            }
        
        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace').strip()
        stderr_text = stderr.decode('utf-8', errors='replace').strip()
        
        success = return_code == 0
        result = {
            "success": success,
            "stdout": stdout_text,
            "stderr": stderr_text,
            "return_code": return_code,
            "command": command,
            "working_dir": working_dir or os.getcwd()
        }
        
        if not success:
            result["error"] = f"Command failed with return code {return_code}"
        
        logger.info(f"Command completed with return code: {return_code}")
        return result
        
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        return {
            "success": False,
            "error": f"Execution error: {str(e)}",
            "stdout": "",
            "stderr": "",
            "return_code": -1,
            "command": command,
            "working_dir": working_dir or os.getcwd()
        }

# Create FastMCP server instance
mcp = FastMCP("Bash Command Server")

@mcp.tool()
async def execute_bash(
    command: str,
    working_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a bash command safely with security restrictions.
    
    This tool allows execution of bash commands with the following safety measures:
    - Command length limits
    - Blocked dangerous commands (rm, sudo, etc.)
    - Blocked dangerous patterns (pipes, redirects, etc.)
    - Execution timeout
    - Limited environment variables
    - Working directory validation
    
    Args:
        command: The bash command to execute (max 1000 characters)
        working_directory: Optional directory to run the command in
        
    Returns:
        Dict containing:
        - success: Boolean indicating if command succeeded
        - stdout: Standard output from the command
        - stderr: Standard error from the command  
        - return_code: Exit code of the command
        - command: The executed command
        - working_dir: The directory where command was executed
        - error: Error message if command failed or was blocked
    """
    return await execute_bash_command(command, working_directory)

@mcp.tool()
async def list_safe_commands() -> List[str]:
    """
    Get a list of commonly used safe commands that can be executed.
    
    Returns:
        List of safe command examples
    """
    return [
        "ls -la",
        "pwd", 
        "whoami",
        "date",
        "echo 'hello world'",
        "cat /etc/os-release",
        "ps aux",
        "df -h",
        "free -h",
        "uptime",
        "which python",
        "python --version",
        "uv --version",
        "git status",
        "git log --oneline -5"
    ]

@mcp.tool()
async def get_security_info() -> Dict[str, Any]:
    """
    Get information about the security measures in place for bash command execution.
    
    Returns:
        Dict containing security configuration details
    """
    return {
        "max_command_length": MAX_COMMAND_LENGTH,
        "timeout_seconds": TIMEOUT_SECONDS,
        "blocked_commands": sorted(list(BLOCKED_COMMANDS)),
        "blocked_patterns": BLOCKED_PATTERNS,
        "environment_variables_available": ["PATH", "HOME", "USER", "PWD"],
        "security_features": [
            "Command length validation",
            "Dangerous command blocking", 
            "Pattern-based filtering",
            "Execution timeout",
            "Limited environment",
            "Working directory validation",
            "Safe character validation"
        ]
    }

if __name__ == "__main__":
    # Run the server with HTTP transport
    import argparse
    
    parser = argparse.ArgumentParser(description="FastMCP 2.0 Bash Command Server")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
    parser.add_argument("--transport", type=str, choices=["http", "stdio"], default="http", 
                       help="Transport type (default: http)")
    
    args = parser.parse_args()
    
    if args.transport == "http":
        logger.info(f"Starting Bash Command Server on http://{args.host}:{args.port}")
        mcp.run(transport="http", port=args.port, host=args.host)
    else:
        logger.info("Starting Bash Command Server with stdio transport")
        mcp.run()