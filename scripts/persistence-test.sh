#!/usr/bin/env bash
# persistence-test.sh
# Verifies that PostgreSQL data persists across a container restart.
set -euo pipefail

echo "=== PostgreSQL Persistence Test ==="

# Register a test user and create a task before restart
echo "Step 1: Registering test user and creating task..."
TEST_EMAIL="persistence-test-$(date +%s)@example.com"
TEST_PASSWORD="PersistTest123"

REGISTER=$(curl --fail --silent --show-error \
  -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Persistence Tester\",\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
echo "Register response: $REGISTER"

LOGIN=$(curl --fail --silent --show-error \
  -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
TOKEN=$(echo "$LOGIN" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Login successful, token obtained."

TASK_TITLE="Persistence check $(date +%s)"
CREATE=$(curl --fail --silent --show-error \
  -X POST http://localhost:3000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"title\":\"$TASK_TITLE\",\"description\":\"Testing PostgreSQL persistence\"}")
TASK_ID=$(echo "$CREATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task']['id'])")
echo "Task created with ID: $TASK_ID, title: $TASK_TITLE"

# Restart the backend and postgres containers
echo ""
echo "Step 2: Restarting backend and postgres containers..."
docker compose restart backend postgres
echo "Containers restarted."

# Wait for backend to be healthy again
echo ""
echo "Step 3: Waiting for backend to become healthy after restart..."
for attempt in $(seq 1 40); do
  if curl --fail --silent http://localhost:3000/health > /dev/null 2>&1; then
    echo "Backend is healthy after restart (attempt $attempt)"
    break
  fi
  if [[ "$attempt" -eq 40 ]]; then
    echo "::error::Backend did not recover after restart"
    docker compose logs backend
    exit 1
  fi
  echo "Waiting for backend ($attempt/40)..."
  sleep 3
done

# Re-login (token may be invalid after restart due to stateless JWT, but data should persist)
echo ""
echo "Step 4: Re-authenticating after restart..."
LOGIN2=$(curl --fail --silent --show-error \
  -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
TOKEN2=$(echo "$LOGIN2" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
echo "Re-authentication successful."

# Verify the task still exists
echo ""
echo "Step 5: Verifying task persisted after restart..."
TASKS=$(curl --fail --silent --show-error \
  -X GET http://localhost:3000/api/tasks \
  -H "Authorization: Bearer $TOKEN2")
TASK_FOUND=$(echo "$TASKS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tasks = data.get('tasks', [])
found = any(t.get('id') == $TASK_ID for t in tasks)
print('true' if found else 'false')
")

if [[ "$TASK_FOUND" == "true" ]]; then
  echo "PASS: Task ID $TASK_ID found after container restart — PostgreSQL data persisted successfully."
else
  echo "::error::FAIL: Task ID $TASK_ID NOT found after container restart — PostgreSQL data did NOT persist."
  echo "Current tasks: $TASKS"
  exit 1
fi

echo ""
echo "=== PostgreSQL Persistence Test: PASSED ==="
