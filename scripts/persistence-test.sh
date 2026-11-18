#!/usr/bin/env bash
set -euo pipefail

DB_USER="${POSTGRES_USER:-taskflow_user}"
DB_NAME="${POSTGRES_DB:-taskflow}"
PERSIST_EMAIL="persistence-check-$(date +%s)@example.com"

echo "=== Step 1: Inserting test record before restart ==="
docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c \
  "INSERT INTO users (name, email, password_hash) VALUES ('Persistence Tester', '$PERSIST_EMAIL', 'hashed_pw_test');"

echo "=== Step 2: Restarting PostgreSQL container ==="
docker compose restart postgres

echo "=== Step 3: Waiting for PostgreSQL readiness ==="
PG_READY=0
for i in $(seq 1 30); do
  if docker compose exec -T postgres pg_isready -U "$DB_USER" -d "$DB_NAME"; then
    PG_READY=1
    echo "PostgreSQL is ready and accepting connections ($i/30)"
    break
  fi
  echo "Waiting for PostgreSQL ($i/30)..."
  sleep 2
done

if [ "$PG_READY" -ne 1 ]; then
  echo "ERROR: PostgreSQL did not become ready after restart"
  docker compose logs postgres
  exit 1
fi

echo "=== Step 4: Waiting for backend /health endpoint to recover ==="
BACKEND_HEALTHY=0
for i in $(seq 1 30); do
  HEALTH_RESP=$(curl --silent http://localhost:3000/health || true)
  if echo "$HEALTH_RESP" | grep -q '"status":"ok"'; then
    BACKEND_HEALTHY=1
    echo "Backend is healthy: $HEALTH_RESP"
    break
  fi
  echo "Waiting for backend ($i/30)... (last response: $HEALTH_RESP)"
  sleep 2
done

if [ "$BACKEND_HEALTHY" -ne 1 ]; then
  echo "ERROR: Backend /health did not recover after PostgreSQL restart"
  docker compose logs backend
  docker compose logs postgres
  exit 1
fi

echo "=== Step 5: Verifying test record survived restart ==="
FOUND=$(docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -t -A -c \
  "SELECT email FROM users WHERE email = '$PERSIST_EMAIL';")

if [ "$FOUND" = "$PERSIST_EMAIL" ]; then
  echo "SUCCESS: PostgreSQL persistence confirmed! Record '$FOUND' survived container restart."
else
  echo "ERROR: Persistence check failed. Record '$PERSIST_EMAIL' was not found after restart!"
  docker compose exec -T postgres psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT * FROM users;"
  exit 1
fi
