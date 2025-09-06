#!/usr/bin/env python3
"""
Example usage of the FastMCP 2.0 Bash Command Server

This demonstrates how to use the server's core functionality.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from bash_command_server import execute_bash_command, BLOCKED_COMMANDS, MAX_COMMAND_LENGTH, TIMEOUT_SECONDS

async def demo_server_usage():
    """Demonstrate the server's capabilities."""
    
    print("FastMCP 2.0 Bash Command Server Demo")
    print("=" * 40)
    
    # Show security information  
    print("\n1. Security Configuration:")
    print(f"   Max command length: {MAX_COMMAND_LENGTH} chars")
    print(f"   Timeout: {TIMEOUT_SECONDS} seconds")
    print(f"   Blocked commands: {len(BLOCKED_COMMANDS)} items")
    print(f"   Examples: {', '.join(list(BLOCKED_COMMANDS)[:5])}")
    
    # List safe commands
    print("\n2. Safe Commands Examples:")
    safe_commands = [
        "ls -la",
        "pwd", 
        "whoami",
        "date",
        "echo 'hello world'",
        "python --version",
        "uv --version"
    ]
    for cmd in safe_commands[:5]:  # Show first 5
        print(f"   - {cmd}")
    
    # Execute some commands
    print("\n3. Command Execution Examples:")
    
    test_commands = [
        "echo 'Hello from FastMCP!'",
        "pwd", 
        "date",
        "uv --version"
    ]
    
    for cmd in test_commands:
        print(f"\n   Executing: {cmd}")
        result = await execute_bash_command(cmd)
        
        if result["success"]:
            print(f"   ✓ Success: {result['stdout']}")
        else:
            print(f"   ✗ Failed: {result.get('error', 'Unknown error')}")
    
    # Test security blocking
    print("\n4. Security Blocking Demo:")
    dangerous_cmd = "rm -rf /"
    print(f"   Attempting dangerous command: {dangerous_cmd}")
    result = await execute_bash_command(dangerous_cmd)
    print(f"   ✓ Blocked: {result.get('error', 'Command was blocked')}")
    
    print("\n" + "=" * 40)
    print("Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_server_usage())