#!/usr/bin/env bash
set -e

echo "=== Checking Required Submission Files ==="

required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Missing required file: $file"
    exit 1
  fi
  echo "✔ Found: $file"
done

echo "All required files are verified."
