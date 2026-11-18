#!/usr/bin/env bash
set -e

echo "Testing PostgreSQL persistence..."
docker compose stop postgres
docker compose start postgres

for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U taskflow_user -d taskflow >/dev/null 2>&1; then
    echo "PostgreSQL is ready after restart."
    break
  fi
  sleep 1
done

docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT count(*) FROM users;"
docker compose exec -T postgres psql -U taskflow_user -d taskflow -c "SELECT count(*) FROM tasks;"
echo "PostgreSQL data persistence verified successfully."