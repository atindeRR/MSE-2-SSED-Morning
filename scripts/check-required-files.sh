#!/usr/bin/env bash
set -e

echo "Checking required files..."
required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  ".env.example"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "ERROR: Required file '$file' is missing!"
    exit 1
  fi
  echo "? $file exists"
done

echo "All required files are present."