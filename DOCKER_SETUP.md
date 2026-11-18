# TaskFlow morning-shift Docker implementation

Student: Manu Garg · 2400291520149 · CSE-AI-C · CSE (Artificial Intelligence)
GitHub / Docker Hub: mg8273

## Start locally

Use this morning-shift repository, not yesterday's CampusHub mock.

```sh
cp .env.example .env  # only if a local .env does not already exist
# Replace all placeholders with local credentials and set DOCKERHUB_USERNAME=mg8273.
# DATABASE_URL must use the same database username/password as POSTGRES_*.
docker compose up -d --build --wait --wait-timeout 180
```

Application: http://localhost:8080 · API health: http://localhost:3000/health
The frontend also proxies `/api/` and `/health` to the backend.

All application source files, SQL schema and supplied API tests remain unchanged.
The frontend Nginx configuration listens on 8080 so its runtime can run as
non-root. The frontend image contains only Nginx and the compiled React assets.
The backend installs locked production dependencies and runs as Node's non-root
user. Both Dockerfiles use health checks and cache dependency installation
separately from source copies.

## Architecture

Browser → frontend Nginx → backend Express → PostgreSQL / Redis.
The `web` network connects frontend and backend; `data` connects backend,
PostgreSQL and Redis. Only the frontend is published publicly. The backend's
port is bound to host loopback for the provided CI tests. PostgreSQL and Redis
have no host ports. A named `postgres_data` volume persists database state.
The provided SQL schema is mounted read-only into PostgreSQL's initialization
directory, where it runs only on an empty database.

## Verify

```sh
bash scripts/check-required-files.sh
cd tests && npm ci && NODE_OPTIONS=--experimental-vm-modules npm test && cd ..
bash scripts/persistence-test.sh
docker compose ps
```

The persistence script creates a test user and task, runs `docker compose down`
without `-v`, starts the same configuration, and verifies the task survived and
Redis repopulates its cache. It never deletes named volumes.

## Publish and deploy

1. Run `bash scripts/configure-secrets.sh` in your own Terminal. Enter a Docker
   Hub Read & Write access token at its hidden prompt. The script logs in and
   sets DOCKERHUB_USERNAME, DOCKERHUB_TOKEN and POSTGRES_PASSWORD on your fork.
   Do not commit `.env`, tokens, or rendered Compose output.
2. Push the implementation to `mg8273/MSE-2-SSED-Morning`, branch `main`.
3. The provided CD workflow, updated to use secrets and the required image names,
   builds and publishes both AMD64 and ARM64 images. ARM64 supports this Mac;
   AMD64 supports the GitHub-hosted runner. Images have `latest` and commit tags.
4. CD pulls the commit-tagged images, deploys them, verifies health and frontend
   access, runs the supplied API tests and persistence check, then cleans up its
   disposable runner stack.

Required image references:

- `docker.io/mg8273/frontend:latest`
- `docker.io/mg8273/backend:latest`

After successful publication, deploy without building:

```sh
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d --wait --wait-timeout 180
```

The deployment configuration has no `build:` directives. It uses the provided
SQL file from the checked-out repository; no local frontend/backend build is
needed. Both configurations share the project's PostgreSQL volume.

## Upstream evaluation caveat

The paper names `taskflow-docker` in its PR section, but its actual starter and
fork parent are `atindeRR/MSE-2-SSED-Morning`. That actual repository is the
appropriate PR base unless the instructor specifies another destination.

The instructor's supplied CI checks out evaluation scripts from its own main
branch, but that starter currently lacks `scripts/check-required-files.sh` and
`scripts/persistence-test.sh`. This submission supplies those scripts for local
and fork-side evaluation. The upstream instructor-controlled CI still needs
those files on the instructor's main branch; submission code cannot repair
that external condition. The instructor CI workflow is preserved unchanged.

## Submission

See `SUBMISSION_CHECKLIST.md`. The PDF is mandatory, must include real CI/CD
screenshots, and must be attached to the final PR and submitted on Moodle.
A local pass alone does not satisfy publication or CD requirements.

## Recorded verification

- Supplied API tests: 12/12 passed.
- PostgreSQL task survived down/up; Redis cache repopulation passed.
- Both Dockerfiles passed the current instructor Hadolint checks.
- Fork CI passed: https://github.com/mg8273/MSE-2-SSED-Morning/actions/runs/44240512562
- CD passed: https://github.com/mg8273/MSE-2-SSED-Morning/actions/runs/44240555155
- Both public Docker Hub images provide AMD64 and ARM64 variants.
- Published-image deployment passed on this Apple Silicon Mac.
- Final PDF: evidence/2400291520149_Manu_Garg.pdf. Review before Moodle upload.
