#!/bin/bash
set -e
files=(
  frontend/Dockerfile
  backend/Dockerfile
  docker-compose.yml
  docker-compose.deploy.yml
  frontend/nginx.conf
  backend/db/init.sql
  tests/package.json
)
for file in "${files[@]}"; do
  test -f "$file" || { echo "Missing required file: $file"; exit 1; }
done
echo "All required files are present."
