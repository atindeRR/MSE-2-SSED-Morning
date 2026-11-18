#!/bin/bash
set -e
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c \
"CREATE TABLE IF NOT EXISTS persistence_check (id INT PRIMARY KEY, value TEXT); INSERT INTO persistence_check VALUES (1, 'persisted') ON CONFLICT (id) DO UPDATE SET value = EXCLUDED.value;"
docker compose restart postgres
for i in $(seq 1 20); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow >/dev/null 2>&1; then
    break
  fi
  sleep 2
done
RESULT=$(docker compose exec -T postgres psql -U taskflow_user -d taskflow -tAc "SELECT value FROM persistence_check WHERE id=1")
test "$RESULT" = "persisted"
echo "PostgreSQL persistence test passed."
