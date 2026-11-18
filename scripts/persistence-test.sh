#!/usr/bin/env bash
set -e

echo "Starting PostgreSQL persistence verification..."

echo "Stopping containers (preserving volumes)..."
docker compose down

echo "Restarting application stack from existing volume..."
docker compose up -d

echo "Waiting for stack to become healthy..."
for attempt in $(seq 1 40); do
  if curl --fail --silent http://localhost:3000/health > /dev/null; then
    echo "Stack is healthy after restart ($attempt/40)"
    echo "PostgreSQL persistence test passed successfully."
    exit 0
  fi
  sleep 2
done

echo "Error: Backend failed to become healthy after restart"
docker compose ps
docker compose logs --no-color
exit 1
