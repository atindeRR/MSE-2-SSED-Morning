#!/usr/bin/env bash
# check-required-files.sh
# Verifies that all required Docker and Compose files are present in the submission.
set -euo pipefail

PASS=0
FAIL=0

check_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    echo "  PRESENT: $file"
    PASS=$((PASS + 1))
  else
    echo "::error::MISSING required file: $file"
    FAIL=$((FAIL + 1))
  fi
}

check_dir() {
  local dir="$1"
  if [[ -d "$dir" ]]; then
    echo "  PRESENT: $dir/"
    PASS=$((PASS + 1))
  else
    echo "::error::MISSING required directory: $dir"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Checking required submission files ==="

check_file "frontend/Dockerfile"
check_file "backend/Dockerfile"
check_file "docker-compose.yml"
check_file "docker-compose.deploy.yml"
check_file "backend/db/init.sql"
check_file "backend/src/server.js"
check_file "backend/package.json"
check_file "frontend/package.json"

echo ""
echo "=== Checking Compose files reference required services ==="

for svc in frontend backend postgres redis; do
  if grep -q "$svc" docker-compose.yml; then
    echo "  PRESENT service in docker-compose.yml: $svc"
    PASS=$((PASS + 1))
  else
    echo "::error::Service '$svc' not found in docker-compose.yml"
    FAIL=$((FAIL + 1))
  fi
done

if grep -q "image:" docker-compose.deploy.yml; then
  echo "  PRESENT: docker-compose.deploy.yml uses image: directives"
  PASS=$((PASS + 1))
else
  echo "::error::docker-compose.deploy.yml must reference published Docker Hub images using image: directives"
  FAIL=$((FAIL + 1))
fi

if grep -Eq "^[[:space:]]+build:" docker-compose.deploy.yml; then
  echo "::error::docker-compose.deploy.yml must NOT contain build: directives (use published images only)"
  FAIL=$((FAIL + 1))
else
  echo "  OK: docker-compose.deploy.yml contains no build: directives"
  PASS=$((PASS + 1))
fi

echo ""
echo "=== Checking volume configuration for PostgreSQL persistence ==="
if grep -q "volumes:" docker-compose.yml; then
  echo "  PRESENT: volumes section in docker-compose.yml"
  PASS=$((PASS + 1))
else
  echo "::error::docker-compose.yml must define named volumes for PostgreSQL data persistence"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Results: $PASS check(s) passed, $FAIL check(s) failed ==="

if [[ "$FAIL" -gt 0 ]]; then
  echo "::error::Required file or configuration check failed — $FAIL issue(s) found"
  exit 1
fi

echo "All required files are present and configuration checks passed."
