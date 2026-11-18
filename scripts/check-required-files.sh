#!/usr/bin/env bash
set -euo pipefail

for file in frontend/Dockerfile backend/Dockerfile docker-compose.yml docker-compose.deploy.yml; do
  if [[ ! -s "$file" ]]; then
    echo "Required file is missing or empty: $file" >&2
    exit 1
  fi
  printf 'Found %s\n' "$file"
done
