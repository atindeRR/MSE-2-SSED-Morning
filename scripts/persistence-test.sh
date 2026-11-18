#!/usr/bin/env bash
set -euo pipefail

test_email="persistence-$(date +%s)-$$@example.com"

query_db() {
  docker compose exec -T postgres sh -c \
    'exec psql -X -qAt -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$@"' \
    sh -v "test_email=$test_email"
}

query_db <<'SQL'
WITH test_user AS (
  INSERT INTO users (name, email, password_hash)
  VALUES ('Persistence check', :'test_email', 'test-fixture')
  RETURNING id
)
INSERT INTO tasks (user_id, title)
SELECT id, 'Persisted TaskFlow task' FROM test_user;
SQL

docker compose down
docker compose up -d --no-build --wait --wait-timeout 120

retained_title=$(query_db <<'SQL'
SELECT tasks.title FROM tasks JOIN users ON users.id = tasks.user_id
WHERE users.email = :'test_email';
SQL
)

if [[ "$retained_title" != 'Persisted TaskFlow task' ]]; then
  echo 'PostgreSQL did not retain the test task' >&2
  exit 1
fi

query_db <<'SQL'
DELETE FROM users WHERE email = :'test_email';
SQL

echo "PostgreSQL persistence verified: $retained_title"
