#!/usr/bin/env bash
set -euo pipefail

echo "=== Verifying required files exist ==="
test -f frontend/Dockerfile || (echo "ERROR: Missing frontend/Dockerfile" && exit 1)
test -f backend/Dockerfile || (echo "ERROR: Missing backend/Dockerfile" && exit 1)
test -f docker-compose.yml || (echo "ERROR: Missing docker-compose.yml" && exit 1)
test -f docker-compose.deploy.yml || (echo "ERROR: Missing docker-compose.deploy.yml" && exit 1)

echo "All required configuration files exist."
