# Project Analysis — TaskFlow (MSE-2 Morning Shift)

## 1. Overview

**Subject:** Software Engineering and DevOps (AI310B)  
**Examination:** MSE-2 Final Practical — Morning Shift  
**Starter Repository:** `https://github.com/atindeRR/MSE-2-SSED-Morning`  
**Application Name:** TaskFlow (Full-Stack Task Management Application with Authentication & Caching)

This document summarizes the complete inspection of the repository before implementing Dockerfiles, Docker Compose orchestration, Docker Hub publishing, and CI/CD verification.

---

## 2. Repository Structure

```text
MSE-2/
├── .env.example                     # Sample environment variables for local & container setup
├── .gitignore                       # Ignores node_modules, .env, .DS_Store, coverage, dist
├── README.md                        # Examination problem statement and submission guidelines
├── .github/
│   └── workflows/
│       ├── ci.yml                   # Instructor PR evaluation (hadolint, compose, tests, persistence)
│       └── cd.yml                   # Student push-to-main CD workflow (build, push, deploy, verify)
├── backend/
│   ├── .dockerignore                # Existing Docker ignore rules (node_modules, npm-debug.log, .env, tests)
│   ├── Dockerfile                   # Empty placeholder (to be implemented)
│   ├── package.json                 # Node.js ES modules Express API (no package-lock.json)
│   ├── db/
│   │   └── init.sql                 # PostgreSQL schema initialization (users & tasks tables + index)
│   └── src/
│       ├── app.js                   # Express routes, JWT auth, PostgreSQL queries, Redis cache
│       ├── auth.js                  # JWT Bearer token middleware (requireAuth)
│       ├── config.js                # Environment variable configuration loader
│       ├── db.js                    # PostgreSQL connection pool + retry waitForDatabase()
│       ├── redis.js                 # Redis client + retry connectRedis()
│       └── server.js                # Entrypoint: waits for DB & Redis, starts HTTP server on 0.0.0.0
├── frontend/
│   ├── .dockerignore                # Existing Docker ignore rules (node_modules, dist, npm-debug.log, .env)
│   ├── Dockerfile                   # Empty placeholder (to be implemented)
│   ├── index.html                   # Vite HTML entrypoint
│   ├── nginx.conf                   # Preconfigured Nginx SPA + reverse proxy (/api/ & /health -> backend:3000)
│   ├── package.json                 # React 18 + Vite 5 SPA (no package-lock.json)
│   ├── vite.config.js               # Vite React plugin configuration (outputs to dist/)
│   └── src/
│       ├── main.jsx                 # React SPA calling relative /api endpoints
│       └── style.css                # Application styles
└── tests/
    ├── api.test.js                  # 12 Jest + Supertest end-to-end API & Redis caching tests
    ├── jest.config.js               # Jest configuration
    ├── package.json                 # Test suite dependencies
    └── package-lock.json            # Lockfile for test suite
```

---

## 3. Application Architecture & Technology Stack

| Layer | Technology | Version / Runtime | Directory / Image |
|---|---|---|---|
| **Frontend** | React.js + Vite, served by Nginx | React 18.3, Vite 5.4, Node 20 (build), Nginx 1.27 Alpine (serve) | `./frontend` |
| **Backend** | Node.js + Express.js (ES Modules) | Node 20 Alpine, Express 4.21, `pg` 8.13, `redis` 4.7, `jsonwebtoken` 9, `bcryptjs` 2.4 | `./backend` |
| **Database** | PostgreSQL | `postgres:16-alpine` | Official image + `./backend/db/init.sql` |
| **Cache** | Redis | `redis:7-alpine` | Official image |
| **Testing** | Jest + Supertest | Jest 29.7, Supertest 7.0 | `./tests` |

---

## 4. Service Inventory & Configuration Details

| Component | Directory / Image | Build / Start Command | Container Port | Host Port |
|---|---|---|---|---|
| **frontend** | `./frontend` | Build: `npm run build` (`vite build` -> `dist/`); Serve: `nginx -g 'daemon off;'` | `80` | `8080` |
| **backend** | `./backend` | Start: `npm start` (`node src/server.js`) | `3000` | `3000` |
| **postgres** | `postgres:16-alpine` | Default PostgreSQL entrypoint + `/docker-entrypoint-initdb.d/init.sql` | `5432` | *Internal only (not exposed)* |
| **redis** | `redis:7-alpine` | `redis-server` | `6379` | *Internal only (not exposed)* |

### Port Mapping Rationale
- **Frontend (`8080:80`):** Required by both `.github/workflows/ci.yml` (`curl http://localhost:8080/`) and `.github/workflows/cd.yml` (`curl http://localhost:8080/`). `frontend/nginx.conf` listens on port `80`.
- **Backend (`3000:3000`):** Required by `.env.example` (`PORT=3000`), `backend/src/config.js`, `ci.yml`, `cd.yml` (`curl http://localhost:3000/health`), and `tests/api.test.js` (`BASE_URL=http://localhost:3000`).
- **PostgreSQL (`5432`) & Redis (`6379`):** Kept strictly inside the internal Docker bridge network for security (no unnecessary public host exposure).

---

## 5. Environment Variables

Derived from `.env.example`, `backend/src/config.js`, `.github/workflows/ci.yml`, and `.github/workflows/cd.yml`:

| Variable | Used By | Purpose | Example / Default |
|---|---|---|---|
| `POSTGRES_DB` | `postgres` | Database name created on startup | `taskflow` |
| `POSTGRES_USER` | `postgres` | PostgreSQL user | `taskflow_user` |
| `POSTGRES_PASSWORD` | `postgres` | PostgreSQL user password (secret) | *(provided via `.env` / GitHub Secret)* |
| `DATABASE_URL` | `backend` | PostgreSQL connection string using Compose service name `postgres` | `postgresql://taskflow_user:<pw>@postgres:5432/taskflow` |
| `REDIS_URL` | `backend` | Redis connection string using Compose service name `redis` | `redis://redis:6379` |
| `JWT_SECRET` | `backend` | Secret key used to sign and verify JWT tokens | *(provided via `.env`)* |
| `PORT` | `backend` | Port Express listens on (`0.0.0.0`) | `3000` |
| `DOCKERHUB_USERNAME` | `docker-compose.deploy.yml` | Docker Hub username for pulling published images in CD/deploy | *(provided via `.env` / GitHub Secret)* |

---

## 6. Service Dependencies & Communication Flow

```text
Browser (User)
   │
   ▼  HTTP :8080
┌──────────────────────┐
│  frontend (Nginx:80) │  Serves React static bundle (/usr/share/nginx/html)
│                      │  SPA fallback: try_files $uri $uri/ /index.html
└──────────┬───────────┘
           │  Reverse proxy /api/* and /health -> http://backend:3000/*
           ▼  Docker internal DNS (taskflow-net)
┌──────────────────────┐
│ backend (Express:3000)│  REST API + JWT Auth + Cache-Aside Logic
└────┬────────────┬────┘
     │            │
     │ TCP :5432  │ TCP :6379
     ▼            ▼
┌──────────┐  ┌──────────┐
│ postgres │  │  redis   │
│ (Volume) │  │ (Cache)  │
└──────────┘  └──────────┘
```

### Dependency Order
1. **`postgres`** starts first, initializes schema from `backend/db/init.sql`, and passes `pg_isready` health check.
2. **`redis`** starts and passes `redis-cli ping` health check.
3. **`backend`** depends on `postgres` (`service_healthy`) and `redis` (`service_healthy`), binds `0.0.0.0:3000`, and passes `/health` health check.
4. **`frontend`** depends on `backend` (`service_healthy`) so Nginx can resolve the `backend` upstream hostname cleanly on startup.

---

## 7. API & Health Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | Public | Runs `SELECT 1` on PostgreSQL and `PING` on Redis; returns `200 {"status":"ok","postgres":"ok","redis":"ok"}` or `503` |
| `POST` | `/api/auth/register` | Public | Registers user (`name`, `email`, `password >= 6 chars`) with bcrypt hash; returns `201` or `409` on duplicate email |
| `POST` | `/api/auth/login` | Public | Authenticates user and returns signed JWT (`8h` expiry) + user object |
| `GET` | `/api/tasks` | Bearer JWT | Cache-aside read: returns `{ tasks, source: 'redis-cache' }` on cache hit, or queries PostgreSQL, caches in Redis (`EX: 30`), and returns `{ tasks, source: 'postgres' }` |
| `POST` | `/api/tasks` | Bearer JWT | Creates a task in PostgreSQL and invalidates `tasks:user:<id>` in Redis |
| `PATCH` | `/api/tasks/:id` | Bearer JWT | Updates `title`, `description`, or `status` (`Pending`, `In Progress`, `Completed`) and invalidates Redis cache |
| `DELETE` | `/api/tasks/:id` | Bearer JWT | Deletes task owned by user and invalidates Redis cache |

---

## 8. CI/CD Workflows Overview

### A. Continuous Deployment (`.github/workflows/cd.yml`)
- **Trigger:** `push` to `main`, or manual `workflow_dispatch`.
- **Required GitHub Secrets:** `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (plus `POSTGRES_PASSWORD` per assignment guidelines).
- **Stages:**
  1. Checkout repository.
  2. Validate `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets exist.
  3. Set up Docker Buildx (`docker/setup-buildx-action@v3`).
  4. Login to Docker Hub (`docker/login-action@v3`).
  5. Build and push backend image as `${DOCKERHUB_USERNAME}/taskflow-backend:latest` and `:${GITHUB_SHA}`.
  6. Build and push frontend image as `${DOCKERHUB_USERNAME}/taskflow-frontend:latest` and `:${GITHUB_SHA}`.
  7. Generate deployment `.env` containing `POSTGRES_*`, `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET`, `PORT`, and `DOCKERHUB_USERNAME`.
  8. Validate `docker-compose.deploy.yml` uses `image:` and contains NO `build:` directives, and passes `docker compose -f docker-compose.deploy.yml config --quiet`.
  9. Pull published images (`docker compose -f docker-compose.deploy.yml pull`).
  10. Start deployment stack (`docker compose -f docker-compose.deploy.yml up -d`).
  11. Verify `http://localhost:3000/health` and `http://localhost:8080/`.
  12. Run all 12 Jest/Supertest API & Redis tests (`tests/api.test.js`) against `http://localhost:3000`.
  13. Write Docker Hub publication summary and clean up containers.

### B. Continuous Integration Evaluation (`.github/workflows/ci.yml`)
- **Trigger:** `pull_request` to `main` or `workflow_dispatch`.
- **Key Checks:**
  1. Checks `submission.json` (prints warning if absent).
  2. Runs instructor's `check-required-files.sh`.
  3. Lints BOTH `frontend/Dockerfile` and `backend/Dockerfile` using **`hadolint/hadolint`**.
  4. Creates `.env`, validates `docker compose config --quiet`, runs `docker compose build` and `docker compose up -d`.
  5. Verifies backend (`http://localhost:3000/health`) and frontend (`http://localhost:8080/`).
  6. Runs API & Redis tests and PostgreSQL persistence test.

---

## 9. Potential Issues Identified & Planned Solutions

| # | Potential Issue | Root Cause | Solution |
|---|---|---|---|
| 1 | `npm ci` failing during Docker build | Neither `frontend/` nor `backend/` contains a `package-lock.json` file | Use `npm install --no-audit --no-fund` (frontend build stage) and `npm install --omit=dev --no-audit --no-fund` (backend) |
| 2 | `hadolint` failing CI evaluation | `ci.yml` runs `hadolint/hadolint` strictly on both Dockerfiles | Pin image versions (`node:20-alpine`, `nginx:1.27-alpine`), follow all Hadolint best practices, and locally test both Dockerfiles against `hadolint/hadolint` |
| 3 | Missing PostgreSQL tables on startup | Backend does not execute `init.sql` programmatically | Mount `./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro` in both `docker-compose.yml` and `docker-compose.deploy.yml` |
| 4 | Nginx startup crash (`host not found in upstream "backend"`) | `frontend/nginx.conf` proxies to `http://backend:3000` at config parse time | Set `depends_on: backend: condition: service_healthy` in Compose |
| 5 | Docker Hub image naming mismatch between README and `cd.yml` | README lists `<user>/frontend` & `<user>/backend`, whereas `cd.yml` pushes `<user>/taskflow-frontend:latest` & `<user>/taskflow-backend:latest` | Configure `docker-compose.deploy.yml` to use `${DOCKERHUB_USERNAME}/taskflow-frontend:latest` and `${DOCKERHUB_USERNAME}/taskflow-backend:latest` (matching `cd.yml`), AND additionally push `<user>/frontend:latest` and `<user>/backend:latest` to Docker Hub so both naming conventions are satisfied |
| 6 | PR Base Repository naming mismatch | Starter repo is `atindeRR/MSE-2-SSED-Morning`, while README mentions `taskflow-docker` | Verify fork parent relationship (`atindeRR/MSE-2-SSED-Morning`, branch `main`) explicitly with the student before opening the PR |

---

## 10. Docker Implementation Plan

1. **Phase 2:** Write multi-stage `frontend/Dockerfile` (`node:20-alpine` -> `nginx:1.27-alpine`) using the provided `frontend/nginx.conf`, and review/enhance `frontend/.dockerignore`.
2. **Phase 3:** Write production `backend/Dockerfile` (`node:20-alpine`, non-root `node` user, built-in `HEALTHCHECK`), and review/enhance `backend/.dockerignore`.
3. **Phase 4 & 5:** Create `docker-compose.yml` with custom bridge network, named PostgreSQL volume (`postgres_data`), `init.sql` mount, health checks on all services, and secure `.env`-driven configuration. Update `.env.example` and `.gitignore` as needed.
4. **Phase 6:** Validate Dockerfiles with `hadolint`, build and launch locally, run all 12 Jest API/Redis tests, verify browser UI and PostgreSQL persistence across container recreation, and capture evidence in `deployment-evidence/local/`.
5. **Phase 7–10:** Authenticate Docker Hub, publish images, create and test `docker-compose.deploy.yml` using pulled images, configure GitHub fork + Secrets, and verify the GitHub Actions CD pipeline end-to-end.
6. **Phase 11–14:** Prepare and submit Pull Request, generate the mandatory `ROLL_NUMBER_STUDENT_NAME.pdf` with real execution screenshots, and create `VIVA_QUESTIONS.md`, `PRACTICAL_COMMANDS.md`, and `FINAL_SUBMISSION_REPORT.md`.
