#!/usr/bin/env bash
set -e

echo "=== Verifying Required Files ==="

REQUIRED_FILES=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
)

ALL_PRESENT=true

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file"
  else
    echo "✗ Missing: $file"
    ALL_PRESENT=false
  fi
done

if [ "$ALL_PRESENT" = false ]; then
  echo "Error: One or more required files are missing."
  exit 1
fi

echo "All required files verified successfully."
