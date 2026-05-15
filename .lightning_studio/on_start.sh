#!/bin/bash

# Lightning Studios use a default environment, so we install directly.
# Upgrade pip to ensure the best dependency resolution
pip install --upgrade pip

# Install requirements into the default environment
pip install -r requirements.txt

# Run server in the background
nohup python server_api.py > server_unified.log 2>&1 &
