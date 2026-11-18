#!/usr/bin/env bash
set -e
for file in \
  backend/Dockerfile \
  frontend/Dockerfile \
  docker-compose.yml \
  docker-compose.deploy.yml \
  backend/db/init.sql \
  tests/api.test.js
do
  if [ ! -f "$file" ]; then
    echo "Missing required file: $file"
    exit 1
  fi
done
echo "All required files are present."
