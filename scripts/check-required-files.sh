#!/usr/bin/env bash
set -euo pipefail

required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
  "frontend/package.json"
  "backend/package.json"
  "backend/db/init.sql"
  "tests/api.test.js"
  "tests/package.json"
  "scripts/persistence-test.sh"
)

failed=0

for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "PASS: $file"
  else
    echo "FAIL: Missing $file"
    failed=1
  fi
done

if [ "$failed" -ne 0 ]; then
  echo "Required file validation failed."
  exit 1
fi

echo "All required files are present."
