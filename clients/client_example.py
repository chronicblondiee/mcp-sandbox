#!/usr/bin/env python3
"""
Example MCP client that connects to the FastMCP bash command server.

This demonstrates how to interact with the server using the MCP protocol.
Note: This is a conceptual example showing the interaction pattern.
"""

import asyncio
import json

async def example_mcp_interaction():
    """
    Example of how an MCP client would interact with our bash command server.
    
    This shows the expected JSON-RPC messages that would be exchanged.
    """
    
    print("FastMCP Bash Command Server - Client Interaction Example")
    print("=" * 60)
    
    # 1. Server capabilities
    print("\n1. Server provides these tools:")
    tools = [
        {
            "name": "execute_bash",
            "description": "Execute a bash command safely with security restrictions",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The bash command to execute"},
                    "working_directory": {"type": "string", "description": "Optional working directory"}
                },
                "required": ["command"]
            }
        },
        {
            "name": "list_safe_commands",
            "description": "Get examples of safe commands that can be executed",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_security_info",
            "description": "Get information about security measures in place",
            "inputSchema": {"type": "object", "properties": {}}
        }
    ]
    
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # 2. Example tool calls (JSON-RPC format)
    print("\n2. Example MCP tool call messages:")
    
    # Execute bash command
    execute_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "execute_bash",
            "arguments": {
                "command": "echo 'Hello from MCP client!'",
                "working_directory": None
            }
        }
    }
    
    print(f"\nRequest to execute bash command:")
    print(json.dumps(execute_request, indent=2))
    
    # Example response
    execute_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "success": True,
                        "stdout": "Hello from MCP client!",
                        "stderr": "",
                        "return_code": 0,
                        "command": "echo 'Hello from MCP client!'",
                        "working_dir": "/home/brown/ai-sandbox/mcp-sandbox"
                    }, indent=2)
                }
            ]
        }
    }
    
    print(f"\nExpected response:")
    print(json.dumps(execute_response, indent=2))
    
    # 3. Security example
    print("\n3. Security blocking example:")
    
    security_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "execute_bash",
            "arguments": {
                "command": "rm -rf /",
                "working_directory": None
            }
        }
    }
    
    print(f"\nRequest with dangerous command:")
    print(json.dumps(security_request, indent=2))
    
    security_response = {
        "jsonrpc": "2.0",
        "id": 2,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "success": False,
                        "error": "Command blocked for security: Blocked command: rm",
                        "stdout": "",
                        "stderr": "",
                        "return_code": -1,
                        "command": "rm -rf /",
                        "working_dir": "/home/brown/ai-sandbox/mcp-sandbox"
                    }, indent=2)
                }
            ]
        }
    }
    
    print(f"\nExpected security response:")
    print(json.dumps(security_response, indent=2))
    
    # 4. Usage instructions
    print("\n4. How to use this server:")
    print("""
    To use this FastMCP server with an MCP client:
    
    1. Start the server:
       uv run python bash_command_server.py
       
    2. Configure your MCP client to connect via STDIO transport
    
    3. The server will be available with three tools:
       - execute_bash: Run bash commands safely
       - list_safe_commands: Get safe command examples  
       - get_security_info: Get security configuration
       
    4. All commands go through security validation before execution
    
    5. The server runs with timeout protection and environment isolation
    """)

if __name__ == "__main__":
    asyncio.run(example_mcp_interaction())