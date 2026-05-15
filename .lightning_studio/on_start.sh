#!/bin/bash

# Lightning AI Engine Auto-Start Script
# Optimized for Etbaly Prints

echo "🚀 Starting Etbaly AI Engine initialization..."

# 1. Install required system libraries (Headless OpenGL/EGL)
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y libopengl0 libgl1 libegl1 libglib2.0-0

# 2. Update and install Python dependencies
echo "🐍 Installing Python libraries..."
pip install --upgrade pip
pip install -r requirements.txt

# 3. Launch the AI server in the background
echo "⚡ Launching AI Server..."
nohup python server_api.py > server_unified.log 2>&1 &

# 4. Start the Non-Stop Server Daemon (Keep-Alive)
echo "🛡️ Starting Keep-Alive daemon to prevent auto-stop..."
nohup bash -c 'while true; do echo "[$(date)] Keeping Lightning Studio awake... ⚡"; sleep 300; done' > keep_awake.log 2>&1 &

echo "✅ Engine initialization and Keep-Alive backgrounded successfully."