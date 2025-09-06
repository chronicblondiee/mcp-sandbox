#!/bin/bash

# FastMCP 2.0 Bash Command Server Startup Script
# 
# This script starts the bash command server using uv

echo "Starting FastMCP 2.0 Bash Command Server..."
echo "=========================================="
echo ""
echo "Server capabilities:"
echo "- Safe bash command execution"
echo "- Security filtering and validation"  
echo "- Timeout protection (30 seconds)"
echo "- Working directory support"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

# Start the server
cd "$(dirname "$0")"
uv run python src/bash_command_server.py