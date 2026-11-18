#!/usr/bin/env bash
# ---------------------------------------------------------------
# Local end-to-end check that mimics what the CI/CD pipelines do.
#
#   bash scripts/verify-local.sh                           # builds from source
#   bash scripts/verify-local.sh docker-compose.deploy.yml # uses Docker Hub images
#
# Needs: Docker, curl, Node.js (for the Jest API tests) and a ".env" file.
# Take your screenshots while this runs / from the final summary.
# ---------------------------------------------------------------
set -euo pipefail

COMPOSE_FILE="${1:-docker-compose.yml}"
DC=(docker compose -f "$COMPOSE_FILE")
BACKEND_URL="http://localhost:${BACKEND_HOST_PORT:-3000}"
FRONTEND_URL="http://localhost:${FRONTEND_HOST_PORT:-8080}"

step() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }
fail() { printf '\033[1;31mFAILED: %s\033[0m\n' "$*"; "${DC[@]}" ps || true; "${DC[@]}" logs --no-color --tail=60 || true; exit 1; }

wait_for() { # wait_for <url> <label>
  for attempt in $(seq 1 40); do
    if curl --fail --silent "$1" > /dev/null; then echo "$2 is up"; return 0; fi
    echo "Waiting for $2 ($attempt/40)..."; sleep 3
  done
  fail "$2 did not become ready"
}

[ -f .env ] || { echo "Missing .env - run: cp .env.example .env  (and edit it)"; exit 1; }

step "1. Validate Compose file ($COMPOSE_FILE)"
"${DC[@]}" config --quiet && echo "Compose file is valid"

step "2. Start the stack"
if [ "$COMPOSE_FILE" = "docker-compose.deploy.yml" ]; then
  "${DC[@]}" pull
  "${DC[@]}" up -d
else
  "${DC[@]}" up -d --build
fi

step "3. Health + frontend"
wait_for "$BACKEND_URL/health" "backend"
curl --fail --silent "$BACKEND_URL/health"; echo
wait_for "$FRONTEND_URL/" "frontend"
echo "Frontend -> backend through nginx proxy:"
curl --fail --silent "$FRONTEND_URL/health"; echo
"${DC[@]}" ps

step "4. API + Redis cache tests (Jest)"
( cd tests
  if [ -f package-lock.json ]; then npm ci --no-audit --no-fund; else npm install --no-audit --no-fund; fi
  BASE_URL="$BACKEND_URL" NODE_OPTIONS=--experimental-vm-modules npm test ) || fail "API tests failed"

step "5. PostgreSQL persistence (down WITHOUT -v, then up again)"
EMAIL="persist-$(date +%s)@example.com"
curl --fail --silent -X POST "$BACKEND_URL/api/auth/register" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"Persist Test\",\"email\":\"$EMAIL\",\"password\":\"persist123\"}" > /dev/null \
  || fail "could not register persistence test user"
echo "Registered $EMAIL"
"${DC[@]}" down
"${DC[@]}" up -d
wait_for "$BACKEND_URL/health" "backend (after restart)"
curl --fail --silent -X POST "$BACKEND_URL/api/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"persist123\"}" | grep -q '"token"' \
  || fail "user vanished after restart - volume is NOT persisting data"
echo "PERSISTENCE OK: user survived container removal"

step "ALL CHECKS PASSED"
"${DC[@]}" ps
