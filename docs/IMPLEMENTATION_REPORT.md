# TaskFlow DevOps Implementation & Verification Report
## Software Engineering & DevOps (AI310B) — MSE-2 Morning Shift Practical

**Student Name:** Animesh Chandra Srivastava  
**University Roll Number:** 202401100300042  
**Class Roll Number:** 42  
**Section / Branch:** CSE-AI / AIML-B  
**GitHub Repository:** [https://github.com/animesh68/MSE-2-SSED-Morning](https://github.com/animesh68/MSE-2-SSED-Morning)  
**Implementation Branch:** `main`  
**Docker Hub Namespace:** `grog68`  
**Date of Execution:** November 18, 2026  

---

## 1. Executive Summary

This report documents the containerization, orchestration, automated testing, and CI/CD pipeline integration of the **TaskFlow** full-stack web application. The implementation adheres strictly to the specifications established in the MSE-2 Morning Shift Question Paper, fulfilling all 15 examination criteria across Dockerfile engineering, multi-container Docker Compose orchestration, persistent storage verification, Redis caching validation, Docker Hub image publishing under namespace `grog68`, and automated GitHub Actions verification.

---

## 2. Inventory of Implemented Files

| File Path | Description & Purpose |
|:---|:---|
| `frontend/Dockerfile` | Production multi-stage Dockerfile compiling React/Vite and serving via Nginx Alpine |
| `backend/Dockerfile` | Hardened, pinned Node.js 20 Alpine Dockerfile running as non-root user (`1000:1000`) |
| `docker-compose.yml` | Multi-container orchestration (frontend, backend, postgres, redis) with healthchecks |
| `docker-compose.deploy.yml` | Production deployment compose file referencing Docker Hub images (`grog68/*`) without `build:` directives |
| `frontend/package-lock.json` | Deterministic dependency tree locking for frontend packages (`npm ci` compliant) |
| `backend/package-lock.json` | Deterministic dependency tree locking for backend packages (`npm ci` compliant) |
| `frontend/.dockerignore` | Exclusion matrix preventing `node_modules`, `dist`, logs, and `.env` from build context |
| `backend/.dockerignore` | Exclusion matrix preventing `node_modules`, test files, logs, and `.env` from build context |
| `.gitignore` | Standard Git hygiene ignoring `.env`, `dist`, `coverage`, and test results |
| `.github/workflows/cd.yml` | Updated CD pipeline utilizing canonical Docker Hub repo names (`grog68/*`) and GitHub Secrets |
| `submission.json` | Candidate identity metadata file consumed by the CI evaluation script |
| `scripts/generate_pdf.py` | Automated ReportLab script generating the official submission PDF |
| `README.md` | Comprehensive operational documentation, architecture diagrams, and usage guide |

---

## 3. Architecture & Security Decisions

### 3.1 Multi-Stage Frontend Build
- **Build Isolation**: Source code compilation takes place in a dedicated `node:20.18.0-alpine3.20` container.
- **Zero Build-Tool Leaks**: Only static compilation output (`/app/dist`) is transferred to the lightweight `nginx:1.27.2-alpine` runtime container. Node.js binaries and development toolchains are omitted from the published image, drastically reducing vulnerability surface and image footprint (~25 MB vs ~450 MB).
- **Reverse Proxy Routing**: Configured in `frontend/nginx.conf` to proxy `/api/` and `/health` requests to `http://backend:3000/`, avoiding cross-origin resource sharing (CORS) complexities in client environments.

### 3.2 Non-Root Backend Execution
- Base image: `node:20.18.0-alpine3.20`.
- Application executes under UID:GID `1000:1000` (pre-created `node` user in official Alpine images).
- Static security analysis via **Hadolint** confirmed 0 errors, 0 warnings (100% compliance with Docker security best practices).
- Dependencies installed using `npm ci --omit=dev && npm cache clean --force` for immutability.

### 3.3 Container Network Architecture
- Dedicated bridge network `taskflow-network` isolates inter-service traffic.
- **Database Security**: PostgreSQL (`5432`) and Redis (`6379`) do not expose published ports to the host system. Backend accesses them strictly via internal DNS service hostnames (`postgres:5432` and `redis:6379`).
- Host port mappings are restricted to `8080:80` (Frontend Nginx) and `3000:3000` (Backend API direct testing).

### 3.4 Relational Persistence & Caching
- **PostgreSQL Persistence**: Backed by named volume `postgres_data` mapped to `/var/lib/postgresql/data`. Initialized using `backend/db/init.sql` mounted read-only into `/docker-entrypoint-initdb.d/init.sql:ro`.
- **Redis Caching**: User task lists cached under `tasks:user:<id>` with a 30-second TTL. Mutating operations (`POST`, `PATCH`, `DELETE`) immediately invalidate the corresponding user cache key.

---

## 4. Database Compatibility Audit: Neon PostgreSQL

An audit was performed regarding external managed PostgreSQL instances (e.g. Neon Serverless PostgreSQL):
1. **Application Support for `DATABASE_URL`**:
   - `backend/src/config.js` extracts `process.env.DATABASE_URL` directly.
   - `backend/src/db.js` initializes `pg.Pool({ connectionString: config.databaseUrl })`.
2. **SSL Compatibility**:
   - Tested successfully with `?sslmode=require&channel_binding=require`. Node.js uses its trusted system CA bundle to validate the TLS certificate, authenticating cleanly (`SELECT 1` verified).
   - `waitForDatabase()` provides safe retry handling (30 attempts).
3. **Architecture Preservation**:
   - As mandated by the examination rubric, the 4-service Docker Compose architecture (`frontend`, `backend`, `postgres`, `redis`) is strictly preserved as the local evaluation stack. No services have been removed or replaced.
   - Credentials are never hardcoded or committed to version control.

---

## 5. Container Health & Runtime Verification

Execution command:
```bash
docker compose up -d --build
docker compose ps
```

### Actual Container Status Output:
```text
NAME                IMAGE                         COMMAND                  SERVICE    STATUS                    PORTS
taskflow-backend    mse-2-ssed-morning-backend    "docker-entrypoint.s…"   backend    Up 22 seconds (healthy)   0.0.0.0:3000->3000/tcp
taskflow-frontend   mse-2-ssed-morning-frontend   "/docker-entrypoint.…"   frontend   Up 16 seconds (healthy)   0.0.0.0:8080->80/tcp
taskflow-postgres   postgres:16-alpine            "docker-entrypoint.s…"   postgres   Up 28 seconds (healthy)   5432/tcp
taskflow-redis      redis:7-alpine                "docker-entrypoint.s…"   redis      Up 28 seconds (healthy)   6379/tcp
```

### Backend Health Endpoint Verification:
```bash
curl http://localhost:3000/health
```
**Output:**
```json
{"status":"ok","postgres":"ok","redis":"ok"}
```

### Reverse Proxy Verification:
```bash
curl http://localhost:8080/health
```
**Output:**
```json
{"status":"ok","postgres":"ok","redis":"ok"}
```

---

## 6. Automated Test Suite Execution Results

All 12 automated test cases from `tests/api.test.js` were executed against the live containerized stack:

```bash
cd tests
$env:BASE_URL="http://localhost:3000"
$env:NODE_OPTIONS="--experimental-vm-modules"
npm test
```

### Test Execution Output:
```text
> taskflow-tests@1.0.0 test
> jest --runInBand

PASS ./api.test.js (5.909 s)
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (331 ms)
    √ TC02: register a user (622 ms)
    √ TC03: reject duplicate email (400 ms)
    √ TC04: login and receive token (480 ms)
    √ TC05: reject unauthenticated task request (266 ms)
    √ TC06: create a task (306 ms)
    √ TC07: list tasks and populate cache (281 ms)
    √ TC08: subsequent list can be served from Redis (294 ms)
    √ TC09: update task status and invalidate cache (326 ms)
    √ TC10: reject invalid task status (289 ms)
    √ TC11: delete task (279 ms)
    √ TC12: deleted task is no longer in list (275 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
Snapshots:   0 total
Time:        6.068 s
Ran all test suites.
```

---

## 7. PostgreSQL Persistence Test Evidence

To verify database persistence, container recreation was executed while preserving the named volume:

```bash
# Query initial state
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT count(*) FROM users;"
# Output: count = 1

# Destroy and remove container
docker compose stop postgres
docker compose rm -f postgres

# Recreate container from named volume
docker compose up -d postgres

# Query state after recreation
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT count(*) FROM users;"
# Output: count = 1 (Data perfectly preserved across container lifecycle)
```

---

## 8. Docker Hub Publishing & Deployment Stack Verification

Both production images were built, tagged, authenticated, published, and remotely pulled using Docker Hub namespace `grog68`:

| Component | Docker Hub Repository | Tags | Image Digest | Remote Pull Status |
|:---|:---|:---|:---|:---|
| **Backend** | `grog68/backend` | `latest` | `sha256:64b4f63e2c15e56ec1594b61b3a333a45c7eff98bf1e5fb13c6df555f5b5df3d` | Verified OK |
| **Frontend** | `grog68/frontend` | `latest` | `sha256:0dc6ec8aed5a95bf2246f73c3301182f3a97be578b470b84e05b32bcb05a41e4` | Verified OK |

### 8.1 Remote Image Pull Verification:
```bash
docker pull grog68/backend:latest
docker pull grog68/frontend:latest
```
Both images were successfully fetched from the public Docker Hub registry and verified against their cryptographic content digests.

### 8.2 Deployment Compose Verification (`docker-compose.deploy.yml`):
The standalone deployment configuration contains zero build directives and runs strictly from the published Docker Hub images:
```bash
docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
```
All four services (`taskflow-deploy-frontend`, `taskflow-deploy-backend`, `taskflow-deploy-postgres`, `taskflow-deploy-redis`) started cleanly and achieved `healthy` status.

### 8.3 Deployment Test Suite Execution:
The 12-point Jest test suite was re-run against the deployment stack (`taskflow-deploy-backend`):
```text
PASS ./api.test.js (5.897 s)
  TaskFlow deployed API
    √ TC01: health endpoint confirms API, PostgreSQL and Redis (336 ms)
    √ TC02: register a user (501 ms)
    √ TC03: reject duplicate email (417 ms)
    √ TC04: login and receive token (556 ms)
    √ TC05: reject unauthenticated task request (264 ms)
    √ TC06: create a task (287 ms)
    √ TC07: list tasks and populate cache (281 ms)
    √ TC08: subsequent list can be served from Redis (285 ms)
    √ TC09: update task status and invalidate cache (294 ms)
    √ TC10: reject invalid task status (270 ms)
    √ TC11: delete task (266 ms)
    √ TC12: deleted task is no longer in list (290 ms)

Test Suites: 1 passed, 1 total
Tests:       12 passed, 12 total
```
Additionally, PostgreSQL volume persistence was confirmed on `postgres_deploy_data` (`SELECT count(*) FROM users;` returned 1 after container destruction and recreation).

---

## 9. GitHub Actions CI/CD Pipeline Summary

Both GitHub Actions workflows have been executed and verified directly on the personal fork:

### 9.1 CI Workflow (`.github/workflows/ci.yml`)
- **Workflow Run**: [https://github.com/animesh68/MSE-2-SSED-Morning/actions/runs/44249390669](https://github.com/animesh68/MSE-2-SSED-Morning/actions/runs/44249390669)
- **Status**: **Completed Successfully (PASS)**
- **Stages Verified**:
  - `submission.json` Candidate Identity validation.
  - Required files verification (Dockerfiles, Compose files, configs).
  - **Hadolint** linting for frontend and backend Dockerfiles.
  - `docker-compose.yml` config validation.
  - Image build and full multi-container stack boot.
  - Backend health (`/health`) and frontend response (`localhost:8080/`).
  - 12-point Jest test suite execution (`api.test.js`).
  - PostgreSQL volume persistence check.
  - Evaluation summary generation & artifact upload (`docker-practical-results`).

### 9.2 CD Workflow (`.github/workflows/cd.yml`)
- **Workflow Run**: [https://github.com/animesh68/MSE-2-SSED-Morning/actions/runs/44249311290](https://github.com/animesh68/MSE-2-SSED-Morning/actions/runs/44249311290)
- **Status**: **Completed Successfully (PASS)**
- **Stages Verified**:
  - Encrypted GitHub Actions secrets validation (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`).
  - Secure Docker Hub authentication via `docker/login-action@v3`.
  - Multi-platform image build and push for `grog68/backend` and `grog68/frontend` with `latest` and commit SHA tags.
  - Dynamic `.env` generation with cryptographically random JWT secret.
  - `docker-compose.deploy.yml` validation (zero `build:` directives confirmed).
  - Docker Hub remote image pull (`docker compose -f docker-compose.deploy.yml pull`).
  - Full production stack deployment from Docker Hub images.
  - End-to-end integration test execution against deployed Docker Hub images.

---

## 10. Student Declaration

I confirm that the implementation submitted is my own work and that I have tested the containerized application.

**Candidate Signature:** Animesh Chandra Srivastava  
**Date:** November 18, 2026
