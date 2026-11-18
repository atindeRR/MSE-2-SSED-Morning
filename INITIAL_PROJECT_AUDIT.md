# INITIAL PROJECT AUDIT & SYSTEM ARCHITECTURE REPORT
**Repository:** MSE-2-SSED-Morning (TaskFlow Full-Stack Application)  
**Evaluation Scope:** Docker Containerization, Multi-Container Compose, Docker Hub Publishing, and GitHub Actions CI/CD Pipeline Verification  
**Audit Timestamp:** 2026-11-18  

---

## 1. Existing Project Structure

The project is structured as a multi-tier microservice architecture consisting of a React Vite single-page frontend, a Node.js Express REST API backend, PostgreSQL relational database scripts, Jest/Supertest integration test suites, and GitHub Actions CI/CD workflows.

### Complete Repository Tree

```text
MSE-2-SSED-Morning/
├── .env.example                                # Template for environment variables
├── .gitignore                                  # Git exclusion rules (node_modules, .env, dist, etc.)
├── README.md                                   # Practical assignment instructions & guidelines
├── .github/
│   └── workflows/
│       ├── ci.yml                              # PR evaluation workflow (lint, build, compose up, tests)
│       └── cd.yml                              # Deployment workflow (Docker Hub push, image-based pull & deploy)
├── backend/
│   ├── .dockerignore                           # Files excluded from backend Docker context
│   ├── Dockerfile                              # Backend Dockerfile (CURRENTLY EMPTY - 0 BYTES)
│   ├── package.json                            # Backend Node.js dependencies & scripts
│   ├── db/
│   │   └── init.sql                            # PostgreSQL DDL schema (users, tasks tables)
│   └── src/
│       ├── app.js                              # Express application setup, routes, middleware, cache logic
│       ├── auth.js                             # JWT authentication middleware (requireAuth)
│       ├── config.js                           # Centralized configuration reading process.env
│       ├── db.js                               # PostgreSQL connection pool & retry readiness loop
│       ├── redis.js                            # Redis client initialization & retry readiness loop
│       └── server.js                           # Server entrypoint with top-level await & graceful shutdown
├── frontend/
│   ├── .dockerignore                           # Files excluded from frontend Docker context
│   ├── Dockerfile                              # Frontend Dockerfile (CURRENTLY EMPTY - 0 BYTES)
│   ├── index.html                              # Vite HTML entrypoint mounting React root
│   ├── nginx.conf                              # Production Nginx reverse proxy configuration
│   ├── package.json                            # Frontend React dependencies & build scripts
│   ├── vite.config.js                          # Vite build tool configuration with React plugin
│   └── src/
│       ├── main.jsx                            # React root component (auth, task management, UI)
│       └── style.css                           # UI design system & responsive layout styles
└── tests/
    ├── jest.config.js                          # Jest configuration (Node environment, ESM)
    ├── package-lock.json                       # Dependency lockfile for test runner
    ├── package.json                            # Test runner dependencies (Jest, Supertest)
    └── api.test.js                             # 12 automated API integration test cases
```

### Analysis of Current State vs Deliverables
- **Starter Code Status:** Application source code (backend and frontend) is fully functional and complete.
- **Existing Missing Deliverables Required by Tasks:**
  1. `backend/Dockerfile` exists as an empty file (0 bytes).
  2. `frontend/Dockerfile` exists as an empty file (0 bytes).
  3. `docker-compose.yml` is missing (required for Task 2 and CI workflow).
  4. `docker-compose.deploy.yml` is missing (required for Task 4 and CD workflow).
  5. `.env` is omitted from version control (provided as `.env.example`).
  6. Neither `backend` nor `frontend` includes a `package-lock.json` file. Only `tests` has `package-lock.json`.

---

## 2. Frontend Architecture

### 2.1 Technology Stack & Structure
- **Framework:** React 18 (`react: ^18.3.1`, `react-dom: ^18.3.1`).
- **Build Tool:** Vite 5 (`vite: ^5.4.11`, `@vitejs/plugin-react: ^4.3.4`).
- **Styling:** Vanilla CSS (`frontend/src/style.css`) importing Google Fonts (*DM Sans* and *Manrope*), implementing a clean cards-based responsive UI.
- **Serving Engine:** Production Nginx (`frontend/nginx.conf`).

### 2.2 Scripts & Output Directory
- **Development Script:** `vite --host 0.0.0.0` (binds to all interfaces).
- **Production Build Script:** `vite build`.
- **Build Output Directory:** `dist/` (located inside `frontend/dist/`).

### 2.3 Component Logic & State
- Located entirely within `frontend/src/main.jsx`.
- Manages client authentication state using `localStorage` for `token` (JWT) and `user` object.
- Supports user registration, user login, task creation, task status progression (`Pending` -> `In Progress` -> `Completed`), task deletion, and manual list refreshing.
- Features a **Cache Source Indicator** (`Last response source: postgres` vs `redis-cache`) displaying the cache provenance returned by the backend API.

### 2.4 API Communication Pattern
- **Base Endpoint:** Defined as `const API = '/api';` (relative path).
- **Routing Strategy:** The React app does **not** hardcode backend URLs (such as `http://localhost:3000` or `http://backend:3000`). All browser HTTP calls target relative paths `/api/auth/...` and `/api/tasks/...`.
- **Nginx Reverse Proxy (`frontend/nginx.conf`):**
  ```nginx
  server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    location /api/ {
      proxy_pass http://backend:3000/api/;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
      proxy_pass http://backend:3000/health;
    }

    location / {
      try_files $uri $uri/ /index.html;
    }
  }
  ```
- **Architectural Advantages:**
  1. Resolves all Cross-Origin Resource Sharing (CORS) concerns in production environments.
  2. Eliminates client-side build-time environment variable injection for backend hostnames.
  3. Provides Single-Page Application (SPA) client-side routing fallback via `try_files`.
  4. Automatically proxies `/health` checks to the backend if queried via the frontend port.

### 2.5 Existing Environment Variables
- No environment variables are currently referenced or consumed in `frontend/src/main.jsx` or `frontend/vite.config.js`.

---

## 3. Backend Architecture

### 3.1 Technology Stack & Structure
- **Runtime:** Node.js (configured as ES Modules via `"type": "module"` in `package.json`).
- **Web Framework:** Express 4 (`express: ^4.21.2`).
- **Core Dependencies:**
  - `bcryptjs: ^2.4.3`: Password hashing with salt factor 10.
  - `cors: ^2.8.5`: Cross-origin resource sharing middleware.
  - `jsonwebtoken: ^9.0.2`: JWT generation and verification with 8-hour token TTL.
  - `pg: ^8.13.1`: PostgreSQL client with connection pooling.
  - `redis: ^4.7.0`: Redis v4 client for caching.

### 3.2 Startup Sequence & Dependency Readiness
- **Entrypoint:** `backend/src/server.js`.
- **Startup Protocol:**
  ```javascript
  await waitForDatabase();
  await connectRedis();

  const server = app.listen(config.port, '0.0.0.0', () => {
    console.log(`TaskFlow API listening on ${config.port}`);
  });
  ```
- **Readiness Resilience:**
  - `waitForDatabase()` (`backend/src/db.js`): Executes `SELECT 1` in a loop up to 30 attempts with a 2-second delay between attempts (60-second maximum wait).
  - `connectRedis()` (`backend/src/redis.js`): Connects to Redis client in a loop up to 30 attempts with a 1-second delay (30-second maximum wait).
  - The HTTP server does not start listening until both PostgreSQL and Redis connections succeed.
  - Graceful termination handles `SIGTERM` and `SIGINT` by closing the server and invoking `redis.quit()`.

### 3.3 Available Endpoints
| HTTP Method | Route | Auth Required | Description |
|---|---|---|---|
| `GET` | `/health` | No | Probes PostgreSQL (`SELECT 1`) and Redis (`redis.ping()`). Returns `200 OK` with `{ status: 'ok', postgres: 'ok', redis: 'ok' }` or `503 Service Unavailable`. |
| `POST` | `/api/auth/register` | No | Validates name, email, password (min 6 chars). Hashes password and inserts user into DB. Returns `201 Created` or `409 Conflict` (duplicate email). |
| `POST` | `/api/auth/login` | No | Verifies credentials against DB hash. Returns `200 OK` with signed JWT token and user profile. |
| `GET` | `/api/tasks` | Yes (`Bearer <token>`) | Retrieves user's tasks. Checks Redis cache first. If cache miss, queries DB, populates Redis cache (TTL 30s), and returns tasks with source tag (`postgres` or `redis-cache`). |
| `POST` | `/api/tasks` | Yes (`Bearer <token>`) | Creates new task. Invalidates user's Redis cache key (`tasks:user:<id>`). Returns `201 Created`. |
| `PATCH` | `/api/tasks/:id` | Yes (`Bearer <token>`) | Updates title, description, or status (`Pending`, `In Progress`, `Completed`). Invalidates Redis cache. Returns `200 OK`. |
| `DELETE` | `/api/tasks/:id` | Yes (`Bearer <token>`) | Deletes task. Invalidates Redis cache. Returns `200 OK`. |

### 3.4 Authentication Mechanism
- Middleware defined in `backend/src/auth.js` (`requireAuth`).
- Inspects `Authorization: Bearer <token>` header.
- Verifies signature using `config.jwtSecret`. Injects decoded payload `{ id, email }` into `req.user`.

---

## 4. Database Configuration

### 4.1 PostgreSQL Schema (`backend/db/init.sql`)
The database schema defines two relational tables with referential integrity and performance indexing:

```sql
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status VARCHAR(20) NOT NULL DEFAULT 'Pending'
    CHECK (status IN ('Pending', 'In Progress', 'Completed')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
```

### 4.2 Database Initialization & Migrations
- **No Migration Framework:** The codebase contains no ORM or migration tool (such as Prisma, TypeORM, or Knex).
- **Execution Mechanism:** Schema creation depends entirely on PostgreSQL running `init.sql`. In Docker Compose, this is achieved by mounting `./backend/db/init.sql` to the official PostgreSQL initialization directory:
  `/docker-entrypoint-initdb.d/init.sql:ro`.
- **Critical Requirement:** `backend/src/db.js` only executes `SELECT 1` and **does not** run schema creation queries on startup. PostgreSQL must have tables initialized prior to backend queries.

### 4.3 Database Connection Settings
- Configured in `backend/src/config.js` via `process.env.DATABASE_URL`.
- Default connection pattern:
  `postgresql://taskflow_user:change_this_db_password@postgres:5432/taskflow`

---

## 5. Redis Configuration

### 5.1 Client & Connection
- Configured in `backend/src/config.js` via `process.env.REDIS_URL`.
- Default fallback: `redis://localhost:6379`.
- In Docker network: `redis://redis:6379`.

### 5.2 Caching Strategy: Cache-Aside with Write Invalidation
1. **Cache Key Pattern:** `tasks:user:${userId}` (per-user task list namespace).
2. **Read Operations (`GET /api/tasks`):**
   - The backend checks `redis.get(key)`.
   - **Cache Hit:** Returns cached JSON with `{ tasks: [...], source: 'redis-cache' }`.
   - **Cache Miss:** Queries PostgreSQL, writes result to Redis with a 30-second Time-To-Live (`await redis.set(key, JSON.stringify(result.rows), { EX: 30 })`), and returns `{ tasks: [...], source: 'postgres' }`.
3. **Write Operations (`POST`, `PATCH`, `DELETE`):**
   - Directly mutates PostgreSQL.
   - Immediately evicts cache via `await redis.del(cacheKey(req.user.id))`.
   - Ensures consistency between database updates and subsequent client reads.
4. **Health Diagnostics:** `redis.ping()` is executed as part of `/health`.

---

## 6. Existing GitHub Actions Workflow Explanation

The repository contains two distinct GitHub Actions workflows with strict automated validation criteria.

### 6.1 CI Workflow: `ci.yml` (Evaluation & Verification)
- **Workflow Name:** `Docker Practical - CI Evaluation`
- **Trigger:** Pull Requests targeting branch `main` and manual `workflow_dispatch`.
- **Target Runner:** `ubuntu-latest`.
- **Sequential Pipeline Stages:**
  1. **Checkout Code:** Checks out the PR branch commit.
  2. **Checkout Instructor Files:** Clones the instructor's upstream `main` branch into `instructor-evaluation/`.
  3. **Check Required Files:** Executes `bash instructor-evaluation/scripts/check-required-files.sh`.
  4. **Linting Dockerfiles via Hadolint:**
     - `docker run --rm -i hadolint/hadolint < frontend/Dockerfile`
     - `docker run --rm -i hadolint/hadolint < backend/Dockerfile`
     - *Both Dockerfiles must adhere strictly to Hadolint best practices without lint errors.*
  5. **Set up Buildx:** Configures Docker Buildx engine.
  6. **Generate CI Environment:** Writes `.env` containing CI database credentials (`ci_test_password_123`).
  7. **Compose Config Validation:** Executes `docker compose config --quiet`.
  8. **Stack Build & Launch:** Runs `docker compose build` followed by `docker compose up -d`.
  9. **Backend Health Check Polling:** Loops up to 40 attempts (3s intervals = 120s max) verifying `curl --fail --silent http://localhost:3000/health`.
  10. **Frontend Availability Polling:** Loops up to 20 attempts (3s intervals = 60s max) verifying `curl --fail --silent http://localhost:8080/`.
  11. **Run Integration Tests:** Executes `npm install` and `npm test` inside `instructor-evaluation/tests` targeting `BASE_URL: http://localhost:3000`.
  12. **PostgreSQL Persistence Test:** Runs `bash instructor-evaluation/scripts/persistence-test.sh` to ensure data persists across container restarts.
  13. **Log & Artifact Capture:** Captures `docker compose ps` and `docker compose logs` into workflow artifacts.
  14. **Teardown:** Executes `docker compose down -v --remove-orphans`.

### 6.2 CD Workflow: `cd.yml` (Publish & Production Deployment)
- **Workflow Name:** `Docker Practical - Publish and Verify`
- **Trigger:** Push to branch `main` and manual `workflow_dispatch`.
- **Target Runner:** `ubuntu-latest`.
- **Required Secrets:** `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
- **Sequential Pipeline Stages:**
  1. **Secret Validation:** Verifies both `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` are populated.
  2. **Docker Hub Login:** Authenticates using `docker/login-action@v3`.
  3. **Build & Push Backend Image:**
     - Context: `./backend`
     - Image Tags:
       - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-backend:latest`
       - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-backend:${{ github.sha }}`
  4. **Build & Push Frontend Image:**
     - Context: `./frontend`
     - Image Tags:
       - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-frontend:latest`
       - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-frontend:${{ github.sha }}`
  5. **Generate Deployment Environment:** Writes `.env` including `DOCKERHUB_USERNAME=${{ secrets.DOCKERHUB_USERNAME }}`.
  6. **Validate Deployment Compose (`docker-compose.deploy.yml`):**
     - Ensures `image:` is declared.
     - Enforces that no `build:` directive exists (`grep -Eq '^[[:space:]]+build:' docker-compose.deploy.yml` fails if present).
     - Validates syntax with `docker compose -f docker-compose.deploy.yml config --quiet`.
  7. **Pull Published Images:** Runs `docker compose -f docker-compose.deploy.yml pull`.
  8. **Deploy Stack:** Runs `docker compose -f docker-compose.deploy.yml up -d`.
  9. **Verify Deployment Health:** Probes `http://localhost:3000/health` and `http://localhost:8080/`.
  10. **Execute API Tests against Deployed Hub Images:** Runs test suite from `./tests` against `http://localhost:3000`.
  11. **Cleanup:** Executes `docker compose -f docker-compose.deploy.yml down -v --remove-orphans`.

---

## 7. Required Environment Variables

### 7.1 Environment Variable Matrix
| Variable Name | Required By | Description | Development / Compose Value | CI / CD Value |
|---|---|---|---|---|
| `PORT` | Backend | Express HTTP listening port | `3000` | `3000` |
| `POSTGRES_DB` | PostgreSQL, Backend | Database name | `taskflow` | `taskflow` |
| `POSTGRES_USER` | PostgreSQL, Backend | Database master user | `taskflow_user` | `taskflow_user` |
| `POSTGRES_PASSWORD` | PostgreSQL, Backend | Database user password | User defined (`.env`) | Injected by workflow |
| `DATABASE_URL` | Backend | Full PostgreSQL connection URI | `postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}` | Injected in CI `.env` |
| `REDIS_URL` | Backend | Redis connection URI | `redis://redis:6379` | `redis://redis:6379` |
| `JWT_SECRET` | Backend | Secret string for HMAC SHA256 JWTs | Secure random string | Injected in CI `.env` |
| `DOCKERHUB_USERNAME`| Deploy Compose (`cd.yml`)| Docker Hub namespace for images | `${DOCKERHUB_USERNAME}` | Injected in CD `.env` |

### 7.2 Required GitHub Repository Secrets
To allow the automated GitHub Actions CD workflow to succeed upon push, the repository owner must configure:
1. `DOCKERHUB_USERNAME`: The personal Docker Hub account username.
2. `DOCKERHUB_TOKEN`: Personal Access Token generated from Docker Hub with Read/Write/Delete permissions.
3. `POSTGRES_PASSWORD`: Secret database password.

---

## 8. Docker Implementation Requirements

### 8.1 Frontend Dockerfile (`frontend/Dockerfile`)
Must use a multi-stage build following Hadolint rules:
1. **Build Stage (`node:20-alpine`):**
   - Working directory: `/app`.
   - Copy `package*.json`.
   - Run `npm install`.
   - Copy frontend source files.
   - Run `npm run build` (generates `/app/dist`).
2. **Production Stage (`nginx:1.27-alpine`):**
   - Copy custom `nginx.conf` into `/etc/nginx/conf.d/default.conf`.
   - Copy build artifacts from builder `/app/dist` to `/usr/share/nginx/html`.
   - Expose container port `80`.
   - Command: `CMD ["nginx", "-g", "daemon off;"]`.
3. **Hadolint Considerations:** Explicit image version tags (avoid `:latest`), minimize layers.

### 8.2 Backend Dockerfile (`backend/Dockerfile`)
1. **Base Image:** `node:20-alpine`.
2. **Working Directory:** `/app`.
3. **Dependencies:** Copy `package*.json` and execute `npm install --omit=dev`.
4. **Source Code:** Copy `src/` and `db/`.
5. **Security Best Practice:** Switch user to unprivileged non-root user `USER node`.
6. **Port:** Expose `3000`.
7. **Execution Command:** `CMD ["node", "src/server.js"]`.
8. **Hadolint Considerations:** Validated with Hadolint in CI step 53.

### 8.3 Multi-Container Compose (`docker-compose.yml`)
Must orchestrate 4 services on a shared user-defined bridge network:
1. **`postgres`:**
   - Image: `postgres:16-alpine`.
   - Environment: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
   - Volume: `postgres_data:/var/lib/postgresql/data` (for persistence).
   - Init volume: `./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro`.
   - Healthcheck: `pg_isready -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow}`.
2. **`redis`:**
   - Image: `redis:7-alpine`.
   - Healthcheck: `redis-cli ping`.
   - Optional volume for cache state persistence.
3. **`backend`:**
   - Build: `./backend`.
   - Ports: `"3000:3000"`.
   - Environment: `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `PORT`.
   - Dependencies: `postgres` (`condition: service_healthy`), `redis` (`condition: service_healthy`).
   - Healthcheck: `wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1`.
4. **`frontend`:**
   - Build: `./frontend`.
   - Ports: `"8080:80"` (*critical: host port 8080 maps to container port 80*).
   - Dependencies: `backend` (`condition: service_started` or `service_healthy`).

### 8.4 Deployment Compose (`docker-compose.deploy.yml`)
- Strictly forbids the `build:` directive (enforced by `cd.yml` line 75).
- Uses published Docker Hub images:
  - Backend: `${DOCKERHUB_USERNAME}/taskflow-backend:latest`
  - Frontend: `${DOCKERHUB_USERNAME}/taskflow-frontend:latest`
  - PostgreSQL & Redis: Official Docker Hub library images (`postgres:16-alpine`, `redis:7-alpine`).
- Shares identical port bindings (`8080:80`, `3000:3000`), persistent volumes (`postgres_data`), and environment variables.

---

## 9. Potential Compatibility Issues & Critical Pitfalls

### 9.1 Discrepancy in Docker Hub Image Naming (README vs `cd.yml`)
- **README Section 3 (Task 3):** Recommends naming repositories `frontend` and `backend` (e.g., `USERNAME/frontend`, `USERNAME/backend`).
- **Actual CD Workflow (`.github/workflows/cd.yml` lines 47, 56, 118, 119):**
  - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-backend:latest`
  - `${{ secrets.DOCKERHUB_USERNAME }}/taskflow-frontend:latest`
- **Impact:** If `docker-compose.deploy.yml` or Docker Hub repositories use `frontend`/`backend` instead of `taskflow-frontend`/`taskflow-backend`, the CD pipeline will fail during `docker compose -f docker-compose.deploy.yml pull`.
- **Resolution:** All deployment configurations and Docker Hub repositories must strictly use `taskflow-backend` and `taskflow-frontend`.

### 9.2 Hadolint Linter Strictness in CI
- `ci.yml` pipes both Dockerfiles through `hadolint/hadolint`.
- Common causes of failure:
  - Using `:latest` tags or unpinned versions (Rule DL3007 / DL3006).
  - Running package managers without cache cleanup (e.g., `apk add --no-cache`).
  - Missing JSON array syntax in `CMD` (Rule DL3025).
- **Resolution:** Pin all base images to explicit tags (`node:20-alpine`, `nginx:1.27-alpine`), use JSON syntax for `CMD`, and ensure clean layer structures.

### 9.3 Strict Port Mappings for Health Verification
- `ci.yml` and `cd.yml` explicitly execute:
  - `curl --fail --silent http://localhost:3000/health` -> Host port **3000** must map to backend container port 3000.
  - `curl --fail --silent http://localhost:8080/` -> Host port **8080** must map to frontend Nginx container port 80.
- If frontend is exposed on port 80, 5173, or 3001 on the host, CI/CD checks will fail with connection refused.

### 9.4 Nginx Reverse Proxy Upstream Service Naming
- In `frontend/nginx.conf`:
  `proxy_pass http://backend:3000/api/;`
- Nginx relies on Docker's embedded DNS server (`127.0.0.11`) to resolve `backend`.
- The backend service in both `docker-compose.yml` and `docker-compose.deploy.yml` **must be named exactly `backend`**. If named `api` or `server`, Nginx will return HTTP 502 Bad Gateway.

### 9.5 Database Initialization Reliance on Entrypoint Mount
- `backend/src/db.js` does not execute schema migration scripts.
- If `./backend/db/init.sql` is not mounted to `/docker-entrypoint-initdb.d/init.sql:ro` in PostgreSQL, the tables `users` and `tasks` will not exist, causing API tests to fail with table missing errors.

### 9.6 Volume Persistence for CI Persistence Test
- `ci.yml` runs `instructor-evaluation/scripts/persistence-test.sh`.
- The database service in Compose must mount a named Docker volume to `/var/lib/postgresql/data`. Anonymous volumes or absence of volume configuration will fail the persistence test when containers restart.

### 9.7 Missing Lockfiles in Backend & Frontend
- Neither `backend` nor `frontend` includes `package-lock.json`.
- Running `npm ci` in Dockerfiles would fail with `npm error code ENOENT`.
- Dockerfiles must use `npm install` (with `--omit=dev` for backend) rather than `npm ci`.

### 9.8 Missing `submission.json` Warning
- `ci.yml` checks for `submission.json` and emits a workflow warning if omitted. Adding a clean `submission.json` containing student identification metadata ensures complete submission compliance.

---

## 10. Recommended Implementation Sequence

To achieve a 100% compliant and passing implementation, the recommended execution steps are:

```mermaid
flowchart TD
    A[Phase 1: Implement Dockerfiles] --> B[Phase 2: Implement docker-compose.yml]
    B --> C[Phase 3: Implement docker-compose.deploy.yml]
    C --> D[Phase 4: Create submission.json & Local .env]
    D --> E[Phase 5: Local Verification & Tests]
    E --> F[Phase 6: GitHub Repository Secrets Configuration]
    F --> G[Phase 7: Git Commit, Push & Pipeline Verification]
    G --> H[Phase 8: Pull Request Creation & Documentation]
```

### Step-by-Step Action Plan

1. **Phase 1: Implement Compliant Dockerfiles**
   - Populate `backend/Dockerfile` with lightweight `node:20-alpine`, `npm install --omit=dev`, non-root user `USER node`, and `EXPOSE 3000`.
   - Populate `frontend/Dockerfile` with multi-stage build (`node:20-alpine` builder + `nginx:1.27-alpine` production), copying `nginx.conf` and `dist` build output, and `EXPOSE 80`.
   - Verify Hadolint compliance.

2. **Phase 2: Implement Local Docker Compose (`docker-compose.yml`)**
   - Define services: `postgres` (`postgres:16-alpine`), `redis` (`redis:7-alpine`), `backend` (build `./backend`), `frontend` (build `./frontend`).
   - Configure health checks on `postgres` and `redis`.
   - Configure service dependency ordering with `condition: service_healthy`.
   - Configure persistent named volume `postgres_data` and init script mount `./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro`.
   - Expose ports: Backend `"3000:3000"` and Frontend `"8080:80"`.

3. **Phase 3: Implement Production Deployment Compose (`docker-compose.deploy.yml`)**
   - Mirror `docker-compose.yml` services, networks, volumes, and ports.
   - Replace `build:` directives with image references:
     - `${DOCKERHUB_USERNAME}/taskflow-backend:latest`
     - `${DOCKERHUB_USERNAME}/taskflow-frontend:latest`
   - Verify that no `build:` keyword exists in the file.

4. **Phase 4: Create Submission Metadata (`submission.json`) & Local `.env`**
   - Create `submission.json` with student metadata (Name, Roll Number, Section, GitHub Username, Docker Hub Username).
   - Create local `.env` based on `.env.example`.

5. **Phase 5: Local Testing & Verification**
   - Start stack using `docker compose up -d --build`.
   - Verify backend `/health` endpoint returns `{ status: 'ok', postgres: 'ok', redis: 'ok' }`.
   - Verify frontend loads at `http://localhost:8080/`.
   - Run integration tests inside `./tests` using `npm test`.
   - Verify database persistence by restarting the stack.

6. **Phase 6: GitHub Secrets Configuration**
   - In GitHub repository settings, add secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`.

7. **Phase 7: Push & CI/CD Pipeline Execution**
   - Commit files and push to `main` branch.
   - Monitor GitHub Actions `cd.yml` workflow run to ensure successful build, push to Docker Hub, pull, and deployment test.

8. **Phase 8: Pull Request Creation & Documentation**
   - Create Pull Request against the upstream base repository according to the requested naming format:
     `DOCKER-EXAM | ROLL-NUMBER | STUDENT-NAME | SECTION`.
   - Prepare and attach the required submission PDF.
