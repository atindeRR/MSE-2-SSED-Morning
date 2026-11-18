#!/usr/bin/env bash
set -e
echo "Checking PostgreSQL persistence..."
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "CREATE TABLE IF NOT EXISTS ci_persistence_check (id SERIAL PRIMARY KEY, marker TEXT);"
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "INSERT INTO ci_persistence_check (marker) VALUES ('persistence-ok');"
docker compose restart postgres
for i in $(seq 1 20); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT * FROM ci_persistence_check WHERE marker='persistence-ok';"
echo "Persistence check completed."
