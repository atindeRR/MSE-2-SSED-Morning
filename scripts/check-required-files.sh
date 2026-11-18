#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "backend/Dockerfile"
  "backend/package.json"
  "backend/db/init.sql"
  "frontend/Dockerfile"
  "frontend/package.json"
  "frontend/nginx.conf"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  "tests/package.json"
  "tests/api.test.js"
  ".github/workflows/ci.yml"
  ".github/workflows/cd.yml"
)

for file in "${required_files[@]}"; do
  if [ ! -s "$file" ]; then
    echo "ERROR: Required file is missing or empty: $file"
    exit 1
  fi
  echo "OK: $file"
done

echo "All required project files are present."
