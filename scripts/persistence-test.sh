#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "ERROR: .env file is missing."
  exit 1
fi

set -a
source .env
set +a

echo "Creating a PostgreSQL persistence test record..."

marker="ci-persistence-$(date +%s)-$$"

docker compose exec -T postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -v ON_ERROR_STOP=1 \
  -c "CREATE TABLE IF NOT EXISTS ci_persistence_probe (
        probe_id TEXT PRIMARY KEY,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );"

docker compose exec -T postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -v ON_ERROR_STOP=1 \
  -c "INSERT INTO ci_persistence_probe (probe_id)
      VALUES ('$marker');"

echo "Restarting PostgreSQL container..."
docker compose restart postgres

echo "Waiting for PostgreSQL to become ready..."

ready=false
for attempt in $(seq 1 40); do
  if docker compose exec -T postgres pg_isready \
    -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; then
    ready=true
    break
  fi
  sleep 2
done

if [ "$ready" != true ]; then
  echo "ERROR: PostgreSQL did not become ready after restart."
  docker compose logs postgres
  exit 1
fi

echo "Checking whether the record survived the restart..."

result=$(docker compose exec -T postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  -tA \
  -v ON_ERROR_STOP=1 \
  -c "SELECT COUNT(*) FROM ci_persistence_probe WHERE probe_id = '$marker';")

if [ "$result" != "1" ]; then
  echo "ERROR: PostgreSQL data did not persist after restart."
  exit 1
fi

echo "SUCCESS: PostgreSQL data persisted after container restart."
