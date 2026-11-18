# TaskFlow — Production Docker & CI/CD Orchestration
## Software Systems Engineering and DevOps (AI310B) — MSE-2 Practical

A full-stack containerized task management platform engineered with React (Vite), Node.js (Express), PostgreSQL, and Redis caching. Built following production-grade DevSecOps principles: multi-stage Docker builds, non-root execution, automated container health checks, persistent volume storage, and multi-stage GitHub Actions CI/CD workflows for automated build, testing, Docker Hub publishing (`grog68`), and image-based deployment verification.

---

## 1. Project Overview & System Architecture

TaskFlow provides high-performance, containerized task management featuring JWT-based authentication, PostgreSQL relational persistence, and 30-second Redis TTL caching with automatic invalidation upon mutating operations (creation, update, deletion).

```
                      +---------------------------------------+
                      |         Client Web Browser            |
                      +-------------------+-------------------+
                                          |
                                          | HTTP Requests
                                          v
+---------------------------------------------------------------------------------+
| Docker Bridge Network: taskflow-network                                          |
|                                                                                 |
|   +------------------------------------+                                        |
|   |         taskflow-frontend          |                                        |
|   |       (Nginx 1.27.2 Alpine)        |                                        |
|   |    Host Port 8080 -> Port 80       |                                        |
|   +------------------+-----------------+                                        |
|                      |                                                          |
|                      | Reverse Proxy (/api/*, /health)                          |
|                      v                                                          |
|   +------------------------------------+                                        |
|   |          taskflow-backend          |                                        |
|   |      (Node.js 20.18.0 Alpine)      |                                        |
|   |    Host Port 3000 -> Port 3000     |                                        |
|   +--------+-------------------+-------+                                        |
|            |                   |                                                |
|            | TCP (5432)        | TCP (6379)                                     |
|            v                   v                                                |
|   +------------------+   +-------------------+                                  |
|   | taskflow-postgres|   |  taskflow-redis   |                                  |
|   | (Postgres 16-alp)|   | (Redis 7-alpine)  |                                  |
|   | Volume: data     |   | In-memory Cache   |                                  |
|   +------------------+   +-------------------+                                  |
+---------------------------------------------------------------------------------+
```

---

## 2. The Four Docker Services

| Service Name | Base Image | Role & Responsibility | Container Port | Host Port | Non-Root User |
|:---|:---|:---|:---|:---|:---|
| **frontend** | `nginx:1.27.2-alpine` | Serves compiled React SPA assets & acts as reverse proxy for `/api/` and `/health` | `80` | `8080` | `nginx` (default) |
| **backend** | `node:20.18.0-alpine3.20` | Express REST API, JWT auth, business logic, PostgreSQL & Redis client | `3000` | `3000` | `1000:1000` (`node`) |
| **postgres** | `postgres:16-alpine` | Relational database storing users and tasks with foreign key cascading | `5432` | Internal only | `postgres` |
| **redis** | `redis:7-alpine` | In-memory cache for per-user task lists (30s TTL) | `6379` | Internal only | `redis` |

---

## 3. Dockerfile Implementations & Security Hygiene

### Frontend Multi-Stage Dockerfile (`frontend/Dockerfile`)
The frontend utilizes a multi-stage build pattern to optimize image size and security:
1. **Build Stage (`node:20.18.0-alpine3.20`)**:
   - Pinned Alpine base image minimizes attack surface.
   - Copies `package.json` and `package-lock.json` separately to leverage Docker layer caching.
   - Installs dependencies using `npm ci` for repeatable, deterministic builds.
   - Executes `npm run build` to compile the Vite/React application into static assets in `/app/dist`.
2. **Serving Stage (`nginx:1.27.2-alpine`)**:
   - Copies only the production assets (`/app/dist`) into Nginx's document root (`/usr/share/nginx/html`).
   - Copies custom `nginx.conf` providing SPA client-side fallback routing (`try_files $uri $uri/ /index.html;`) and reverse proxying rules.
   - Node.js, npm, and intermediate build tools (`node_modules`) are completely excluded from the final runtime image.

### Backend Hardened Dockerfile (`backend/Dockerfile`)
1. **Base Image**: Pinned `node:20.18.0-alpine3.20` for minimal layer overhead.
2. **Deterministic Dependencies**: Uses `npm ci --omit=dev && npm cache clean --force` to install only runtime dependencies while purging package caches.
3. **Least Privilege Non-Root Execution**: Runs under UID:GID `1000:1000` (pre-configured `node` user in official Node Alpine images), passing static security audits with 0 warnings.
4. **Clean Decoupling**: No secrets or runtime passwords baked into layers; fully parameterized via environment variables.

### Build Hygiene (`.dockerignore` & `.gitignore`)
- Excludes `node_modules`, `.env`, `.env.*`, `.git`, debug logs (`npm-debug.log*`), build artifacts (`dist`, `coverage`), and test outputs.
- `.env.example` remains tracked as a schema template.

---

## 4. Docker Compose Architecture & Networking

The orchestration file `docker-compose.yml` configures:
- **Private Bridge Network (`taskflow-network`)**: Isolated software-defined bridge network enabling service discovery via DNS hostnames (`postgres`, `redis`, `backend`).
- **Network Isolation**: PostgreSQL (`5432`) and Redis (`6379`) are strictly kept internal to the network and never exposed to the host machine.
- **Port Mapping**:
  - `8080:80` for Frontend Nginx entrypoint.
  - `3000:3000` for Backend API direct testing and CI verification.
- **Startup Order & Health Checks**:
  - `postgres`: Health checked with `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}`.
  - `redis`: Health checked with `redis-cli ping`.
  - `backend`: Depends on healthy `postgres` and `redis`. Health checked with HTTP probe on `http://127.0.0.1:3000/health`.
  - `frontend`: Depends on healthy `backend`. Health checked with HTTP probe on `http://127.0.0.1:80/`.

---

## 5. Storage Persistence & Caching Strategy

### PostgreSQL Data Persistence
- Relational schema defined in `backend/db/init.sql` mounted read-only into `/docker-entrypoint-initdb.d/init.sql:ro`.
- Named Docker volume `postgres_data` mapped to `/var/lib/postgresql/data`.
- **Persistence Verification**: When the `postgres` container is stopped, deleted, and recreated, all user and task records remain intact and immediately accessible.

### Redis Caching Strategy
- **Key Schema**: `tasks:user:<userId>`
- **Read Path**: `GET /api/tasks` checks Redis first (`redis.get`). If cached, returns `{ tasks: [...], source: 'redis-cache' }`. If miss, queries PostgreSQL, saves to Redis with `EX: 30` (30-second TTL), and returns `{ tasks: [...], source: 'postgres' }`.
- **Write Path / Invalidation**: `POST /api/tasks`, `PATCH /api/tasks/:id`, and `DELETE /api/tasks/:id` immediately call `redis.del(cacheKey(userId))` to invalidate stale cache.

---

## 6. Environment Variables Configuration

Create a local `.env` file using `.env.example`:

```bash
cp .env.example .env
```

| Variable | Description | Example / Recommended Value |
|:---|:---|:---|
| `POSTGRES_DB` | PostgreSQL database name | `taskflow` |
| `POSTGRES_USER` | PostgreSQL superuser username | `taskflow_user` |
| `POSTGRES_PASSWORD` | Strong database password | `secret_password_123` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://taskflow_user:secret_password_123@postgres:5432/taskflow` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `JWT_SECRET` | Secret token for signing JWT tokens | `random_32_byte_hex_string` |
| `PORT` | Backend application listening port | `3000` |
| `DOCKERHUB_USERNAME` | Docker Hub username for image deployment | `grog68` |

---

## 7. Local Build & Startup Instructions

### 1. Build and Start All 4 Services
```bash
docker compose up -d --build
```

### 2. Verify Container Status & Health
```bash
docker compose ps
```
All four containers (`taskflow-frontend`, `taskflow-backend`, `taskflow-postgres`, `taskflow-redis`) will display `healthy`.

### 3. Verify Application Endpoints
- **Frontend Web UI**: Open [http://localhost:8080/](http://localhost:8080/) in any web browser.
- **Backend Health Check**:
  ```bash
  curl http://localhost:3000/health
  # Expected Response: {"status":"ok","postgres":"ok","redis":"ok"}
  ```
- **Frontend Reverse Proxy Health**:
  ```bash
  curl http://localhost:8080/health
  # Expected Response: {"status":"ok","postgres":"ok","redis":"ok"}
  ```

### 4. Run Test Suite
```bash
cd tests
npm install
npm test
```
All 12 test cases covering registration, authentication, task lifecycle, cache hits, cache invalidation, and data deletion will execute and pass.

---

## 8. Docker Hub Publishing & Image-Based Deployment

### Deployment Configuration (`docker-compose.deploy.yml`)
The deployment Compose file operates **exclusively with pre-built published images** from Docker Hub (`grog68`) and contains **zero `build:` directives**:
- Backend Image: `${DOCKERHUB_USERNAME:-grog68}/backend:${IMAGE_TAG:-latest}`
- Frontend Image: `${DOCKERHUB_USERNAME:-grog68}/frontend:${IMAGE_TAG:-latest}`
- Database: `postgres:16-alpine`
- Cache: `redis:7-alpine`

### Deploying From Docker Hub
```bash
# 1. Pull published images from Docker Hub
docker compose -f docker-compose.deploy.yml pull

# 2. Launch the application stack
docker compose -f docker-compose.deploy.yml up -d

# 3. Verify health
docker compose -f docker-compose.deploy.yml ps
```

---

## 9. Optional Managed Database: Neon PostgreSQL

TaskFlow natively supports cloud-managed PostgreSQL instances such as **Neon Serverless PostgreSQL**.

### Architecture Preservation Note
The primary practical examination architecture requires exactly four local Docker Compose services (`frontend`, `backend`, `postgres`, `redis`). The containerized `postgres` service is the default local database. Neon PostgreSQL is an optional external managed alternative.

### How Neon Integration Operates
1. `backend/src/config.js` and `backend/src/db.js` ingest `DATABASE_URL` directly:
   ```javascript
   export const pool = new Pool({ connectionString: config.databaseUrl });
   ```
2. When configured with a Neon connection string containing `sslmode=require`, `pg` automatically establishes an encrypted TLS session using Node.js's built-in trusted CA store.
3. Connection retry resilience is natively handled by `waitForDatabase()` (retrying up to 30 attempts at 2-second intervals).

---

## 10. CI/CD Pipeline Architecture

### Continuous Integration (`.github/workflows/ci.yml`)
Triggered on pull requests to `main`:
1. Checkouts submitted pull request branch.
2. Validates `submission.json` candidate metadata.
3. Performs Dockerfile linting with **Hadolint** for both backend and frontend.
4. Validates `docker-compose.yml` syntax via `docker compose config --quiet`.
5. Builds images from source and starts all four containers.
6. Probes backend health (`localhost:3000/health`) and frontend response (`localhost:8080/`).
7. Executes full automated Jest/Supertest integration suite against running stack.
8. Tests PostgreSQL volume persistence via container teardown and re-creation.
9. Exports execution artifacts and container logs.

### Continuous Deployment (`.github/workflows/cd.yml`)
Triggered on push to `main`:
1. Authenticates securely to Docker Hub using GitHub Secrets (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).
2. Builds and tags multi-platform images for `backend` and `frontend` (`grog68/backend` and `grog68/frontend` with `latest` and commit SHA tags).
3. Publishes both images directly to Docker Hub repositories.
4. Generates dynamic `.env` configuration using secret `POSTGRES_PASSWORD` and cryptographic `JWT_SECRET`.
5. Validates `docker-compose.deploy.yml` has no `build:` instructions.
6. Pulls published images from Docker Hub.
7. Deploys the image-based stack and executes end-to-end integration tests.

---

## 11. Troubleshooting & Common Pitfalls

1. **Port 8080 Conflict on Windows**:
   - If a host service (such as Apache HTTPD or IIS) is occupying port 8080, stop the conflicting service or verify within the container network using `docker run --rm --network <network> curlimages/curl http://frontend:80/`.
2. **Alpine IPv6 Name Resolution**:
   - Express binds to IPv4 `0.0.0.0`. In Alpine Linux, `localhost` resolves to IPv6 `::1` first. Ensure internal healthchecks target `127.0.0.1` (`http://127.0.0.1:3000/health`) to prevent connection refused errors.
3. **Docker Hub Secrets**:
   - Ensure `DOCKERHUB_USERNAME` (set to `grog68`), `DOCKERHUB_TOKEN` (Personal Access Token), and `POSTGRES_PASSWORD` are configured under **Settings → Secrets and variables → Actions**.
