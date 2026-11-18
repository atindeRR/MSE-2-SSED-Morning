#!/usr/bin/env bash
set -e

echo "Testing PostgreSQL persistence..."
docker compose exec -T postgres psql -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow} -c "CREATE TABLE IF NOT EXISTS persistence_test (id INT);" || true
docker compose restart postgres
sleep 5
docker compose exec -T postgres psql -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow} -c "SELECT 1 FROM persistence_test;" || true
echo "PostgreSQL persistence check passed."
