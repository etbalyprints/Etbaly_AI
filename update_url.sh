#!/bin/bash
read -p "Enter the new Lightning Studio URL: " STUDIO_URL
curl -X POST https://etbaly.yussefrostom.me/api/v1/admin/ai/set-ai-engine-url \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"$STUDIO_URL\"}"
