#!/usr/bin/env bash
set -e

echo "=== Testing PostgreSQL Data Persistence ==="

# Check that PostgreSQL container is running
echo "Checking postgres container status..."
docker compose ps postgres

# Insert a verification record
echo "Inserting persistence test record..."
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "
INSERT INTO users (name, email, password_hash)
VALUES ('Persistence User', 'persistence-ci-check@example.com', 'dummy_hash_for_test')
ON CONFLICT (email) DO NOTHING;
"

# Restart the PostgreSQL container
echo "Restarting PostgreSQL container..."
docker compose restart postgres

# Wait for database readiness
echo "Waiting for PostgreSQL to be ready after restart..."
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow > /dev/null 2>&1; then
    echo "PostgreSQL is ready."
    break
  fi
  sleep 1
done

# Query the record
echo "Verifying data persisted across reboot..."
RECORD_COUNT=$(docker compose exec -T postgres psql -U taskflow_user -d taskflow -t -c "SELECT count(*) FROM users WHERE email='persistence-ci-check@example.com';" | tr -d '[:space:]')

if [ "$RECORD_COUNT" -ge 1 ]; then
  echo "✓ Persistence verified! Found $RECORD_COUNT record(s) for persistence-ci-check@example.com"
else
  echo "✗ Persistence verification failed: record was not found after container restart"
  exit 1
fi

echo "PostgreSQL persistence test completed successfully."
