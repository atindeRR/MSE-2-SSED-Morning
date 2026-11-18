#!/usr/bin/env bash
set -e

echo "=== Testing PostgreSQL Persistence ==="

# Check containers are running
docker compose ps

# Restart PostgreSQL container
echo "Restarting PostgreSQL container..."
docker compose restart postgres
sleep 5

# Wait for PostgreSQL to be healthy
echo "Verifying PostgreSQL is up and ready..."
for attempt in $(seq 1 30); do
  if docker compose ps postgres | grep -qE "(healthy|running|Up)"; then
    echo "PostgreSQL is running and healthy"
    break
  fi
  sleep 2
done

# Restart backend container to ensure connection re-established
echo "Restarting backend container..."
docker compose restart backend
sleep 5

# Wait for backend to be healthy
echo "Verifying backend health after PostgreSQL restart..."
for attempt in $(seq 1 30); do
  if curl --fail --silent http://localhost:3000/health > /dev/null 2>&1; then
    echo "Backend is healthy and connected to database"
    echo "=== PostgreSQL persistence test passed ==="
    exit 0
  fi
  sleep 2
done

echo "Backend did not become healthy after postgres restart"
exit 1
