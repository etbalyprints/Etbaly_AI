#!/bin/bash

# Lightning AI Engine Auto-Stop Script
# Optimized for Etbaly Prints

echo "🛑 Stopping Etbaly AI Engine and Background Processes..."

# 1. Find and kill the AI server process
SERVER_PIDS=$(ps aux | grep "[s]erver_api.py" | awk '{print $2}')

if [ -n "$SERVER_PIDS" ]; then
    kill -9 $SERVER_PIDS
    echo "✅ AI Server stopped (PIDs: $SERVER_PIDS)."
else
    echo "⚠️ No running AI server found."
fi

# 2. Find and kill the Keep-Alive daemon
KEEPALIVE_PIDS=$(ps aux | grep "[s]leep 300" | awk '{print $2}')

if [ -n "$KEEPALIVE_PIDS" ]; then
    kill -9 $KEEPALIVE_PIDS
    echo "✅ Keep-Alive daemon stopped (PIDs: $KEEPALIVE_PIDS)."
else
    echo "⚠️ No running Keep-Alive daemon found."
fi

echo "🏁 All Etbaly AI processes have been terminated safely. Lightning Studio can now auto-stop."