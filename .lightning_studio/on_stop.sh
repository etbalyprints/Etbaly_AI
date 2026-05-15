#!/bin/bash

# Lightning AI Engine Auto-Stop Script

echo "🛑 Stopping Etbaly AI Engine..."

# Find and kill the server process
PIDS=$(ps aux | grep server_api.py | grep -v grep | awk '{print $2}')

if [ -n "$PIDS" ]; then
    kill $PIDS
    echo "✅ AI Server stopped (PIDs: $PIDS)."
else
    echo "⚠️ No running server found."
fi
