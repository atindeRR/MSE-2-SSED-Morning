#!/usr/bin/env bash
set -euo pipefail

echo "Checking required Docker practical files..."

required_files=(
  "frontend/Dockerfile"
  "backend/Dockerfile"
  "docker-compose.yml"
  "docker-compose.deploy.yml"
)

missing=0

for file in "${required_files[@]}"; do
  if [[ -f "$file" ]]; then
    echo "PASS: $file"
  else
    echo "FAIL: $file is missing"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Required files check failed."
  exit 1
fi

echo "All required Docker files are present."
