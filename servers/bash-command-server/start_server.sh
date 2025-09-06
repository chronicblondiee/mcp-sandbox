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
echo "- HTTP transport on port 8000"
echo ""
echo "Server will be available at: http://127.0.0.1:8000"
echo "To stop the server, press Ctrl+C"
echo ""

# Parse command line arguments
PORT=8000
HOST="127.0.0.1"
TRANSPORT="http"

while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --transport)
            TRANSPORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--port PORT] [--host HOST] [--transport http|stdio]"
            exit 1
            ;;
    esac
done

# Start the server
cd "$(dirname "$0")"
echo "Starting server with transport: $TRANSPORT"
if [ "$TRANSPORT" = "http" ]; then
    echo "Server URL: http://$HOST:$PORT"
fi
echo ""
uv run python src/bash_command_server.py --port "$PORT" --host "$HOST" --transport "$TRANSPORT"