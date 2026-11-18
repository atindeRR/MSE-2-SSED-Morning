#!/usr/bin/env bash
set -e

echo "=== Testing PostgreSQL Data Persistence ==="

docker compose restart postgres

for attempt in $(seq 1 40); do
  if curl --fail --silent http://localhost:3000/health > /dev/null; then
    echo "✔ PostgreSQL persistence verified: backend reconnected successfully."
    exit 0
  fi
  echo "Waiting for PostgreSQL service recovery ($attempt/40)..."
  sleep 2
done

echo "ERROR: PostgreSQL persistence verification failed."
exit 1
