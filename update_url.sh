#!/bin/bash

# Etbaly AI Engine URL Update Script
# Updates both 2D and 3D endpoints in the admin backend

read -p "Enter the new Lightning Studio URL (e.g., https://...-8080.proxy.lightning.ai): " STUDIO_URL

if [ -z "$STUDIO_URL" ]; then
    echo "❌ Error: URL cannot be empty."
    exit 1
fi

echo "🔄 Updating Text-to-Image URL..."
curl -X POST https://etbaly.yussefrostom.me/api/v1/admin/ai/set-text-to-image-url \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"$STUDIO_URL\"}"
echo -e "\n"

echo "🔄 Updating Image-to-3D URL..."
curl -X POST https://etbaly.yussefrostom.me/api/v1/admin/ai/set-image-to-3d-url \
     -H "Content-Type: application/json" \
     -d "{\"url\": \"$STUDIO_URL\"}"
echo -e "\n"

echo "✅ Update process complete."
