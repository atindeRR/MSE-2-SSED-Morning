#!/usr/bin/env bash
set -e

echo "Checking required files for MSE-2 Docker practical..."

REQUIRED_FILES=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file"
  else
    echo "✗ Missing required file: $file"
    exit 1
  fi
done

if [ -f "submission.json" ]; then
  echo "✓ Found: submission.json"
fi

echo "All required files verified successfully."
