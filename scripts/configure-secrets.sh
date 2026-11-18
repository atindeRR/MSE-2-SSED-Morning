#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
repo=mg8273/MSE-2-SSED-Morning
username=mg8273
printf 'Enter a Docker Hub access token with Read & Write permissions (hidden): '
IFS= read -r -s token
printf '\n'
test -n "$token"
printf '%s' "$token" | docker login --username "$username" --password-stdin
printf '%s' "$username" | gh secret set DOCKERHUB_USERNAME --repo "$repo"
printf '%s' "$token" | gh secret set DOCKERHUB_TOKEN --repo "$repo"
unset token
python3 - <<'PY' | gh secret set POSTGRES_PASSWORD --repo "$repo"
from pathlib import Path
values = dict(line.split('=', 1) for line in Path('.env').read_text().splitlines() if line and not line.startswith('#'))
print(values['POSTGRES_PASSWORD'], end='')
PY
printf 'Docker login and all three GitHub Actions secrets configured.\n'
