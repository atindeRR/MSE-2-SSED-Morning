#!/usr/bin/env bash
set -e

echo "=== Checking Required Files ==="

REQUIRED_FILES=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  "README.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "[PASS] Found: $file"
  else
    echo "[FAIL] Missing required file: $file"
    exit 1
  fi
done

echo "All required files are verified."
exit 0
