#!/usr/bin/env python3
"""
HTTP Client Example for FastMCP 2.0 Bash Command Server

This demonstrates how to connect to the bash command server via HTTP transport.
"""

import asyncio
import aiohttp
import json
from typing import Any, Dict


class MCPHTTPClient:
    """Simple MCP HTTP client for testing."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/mcp"):
        self.base_url = base_url
        self.session_id = None
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize the MCP session."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            async with session.post(self.base_url, json=payload) as resp:
                result = await resp.json()
                print(f"Initialize response: {result}")
                return result
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {}
            }
            
            async with session.post(self.base_url, json=payload) as resp:
                result = await resp.json()
                print(f"Tools list: {result}")
                return result
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool."""
        async with aiohttp.ClientSession() as session:
            payload = {
                "jsonrpc": "2.0", 
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            async with session.post(self.base_url, json=payload) as resp:
                result = await resp.json()
                print(f"Tool call result: {result}")
                return result


async def demo_http_client():
    """Demonstrate HTTP client usage with the bash command server."""
    
    print("FastMCP 2.0 HTTP Client Demo")
    print("=" * 40)
    print("Connecting to bash command server at http://127.0.0.1:8000/mcp")
    print()
    
    client = MCPHTTPClient()
    
    try:
        # Initialize the connection
        print("1. Initializing MCP session...")
        await client.initialize()
        print()
        
        # List available tools
        print("2. Listing available tools...")
        await client.list_tools()
        print()
        
        # Get security info
        print("3. Getting security information...")
        await client.call_tool("get_security_info", {})
        print()
        
        # List safe commands
        print("4. Listing safe commands...")
        await client.call_tool("list_safe_commands", {})
        print()
        
        # Execute a safe command
        print("5. Executing a safe command...")
        await client.call_tool("execute_bash", {
            "command": "echo 'Hello from HTTP MCP client!'"
        })
        print()
        
        # Test with working directory
        print("6. Testing with working directory...")
        await client.call_tool("execute_bash", {
            "command": "pwd",
            "working_directory": "/tmp"
        })
        print()
        
        print("=" * 40)
        print("HTTP client demo completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the server is running with:")
        print("  cd servers/bash-command-server")
        print("  ./start_server.sh")


if __name__ == "__main__":
    asyncio.run(demo_http_client())