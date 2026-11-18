#!/usr/bin/env bash
set -euo pipefail
for file in frontend/Dockerfile frontend/.dockerignore frontend/package-lock.json backend/Dockerfile backend/.dockerignore backend/package-lock.json docker-compose.yml docker-compose.deploy.yml submission.json; do
  test -s "$file" || { echo "Missing or empty: $file"; exit 1; }
done
if grep -Eq '^[[:space:]]+build:' docker-compose.deploy.yml; then
  echo 'Deployment Compose must use published images, without build directives'
  exit 1
fi
echo 'Required submission files present; deployment Compose uses images.'
