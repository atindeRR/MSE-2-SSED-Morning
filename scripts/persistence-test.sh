#!/usr/bin/env bash
set -euo pipefail

echo "Creating persistence test table and record..."

docker compose exec -T postgres sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1' <<'SQL'
CREATE TABLE IF NOT EXISTS ci_persistence_check (
    id INTEGER PRIMARY KEY,
    marker TEXT NOT NULL
);

INSERT INTO ci_persistence_check (id, marker)
VALUES (1, 'docker-volume-persistence-verified')
ON CONFLICT (id)
DO UPDATE SET marker = EXCLUDED.marker;
SQL

echo "Restarting PostgreSQL container..."
docker compose restart postgres

echo "Waiting for PostgreSQL..."
for attempt in $(seq 1 30); do
  if docker compose exec -T postgres sh -c \
    'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"' >/dev/null 2>&1; then
    break
  fi

  if [ "$attempt" -eq 30 ]; then
    echo "PostgreSQL did not become ready."
    exit 1
  fi

  sleep 2
done

echo "Checking whether the record survived the restart..."

result=$(docker compose exec -T postgres sh -c \
  'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT marker FROM ci_persistence_check WHERE id = 1"')

if [ "$result" = "docker-volume-persistence-verified" ]; then
  echo "SUCCESS: PostgreSQL data persisted after container restart."
else
  echo "FAIL: PostgreSQL persistence verification failed."
  exit 1
fi
