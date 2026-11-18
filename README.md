# TaskFlow — Docker Practical Exam

> **Student:** Vivek Kumar | **Roll:** 2400291520281 | **Section:** D | **Branch:** CSEAI  
> **Course:** Software Engineering and DevOps (AI310B) — MSE-2 Morning Shift  
> **GitHub:** [vivvvekk](https://github.com/vivvvekk) | **Docker Hub:** [vivvvekk](https://hub.docker.com/u/vivvvekk)

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite (served by nginx) |
| Backend | Node.js 20 + Express |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Container | Docker + Docker Compose |

---

## Quick Start (Local Build)

### Prerequisites
- Docker Desktop ≥ 24 with Compose v2

### 1. Clone & configure

```bash
git clone https://github.com/vivvvekk/MSE-2-SSED-Morning.git
cd MSE-2-SSED-Morning
cp .env.example .env
# Edit .env and set your own POSTGRES_PASSWORD and JWT_SECRET
```

### 2. Build & run

```bash
docker compose up -d --build
```

### 3. Verify

```bash
docker compose ps              # all 4 services healthy
curl http://localhost:3000/health   # {"status":"ok","postgres":"ok","redis":"ok"}
curl http://localhost:8080/         # returns HTML
```

### 4. Tear down (keeps data)

```bash
docker compose down
```

### 5. Tear down with data wipe

```bash
docker compose down -v
```

---

## Deploy from Docker Hub

```bash
# Set required env vars
export DOCKERHUB_USERNAME=vivvvekk
export POSTGRES_PASSWORD=your_secure_password
export DATABASE_URL=postgresql://taskflow_user:${POSTGRES_PASSWORD}@postgres:5432/taskflow
export JWT_SECRET=your_long_random_secret

docker compose -f docker-compose.deploy.yml pull
docker compose -f docker-compose.deploy.yml up -d
```

---

## Docker Hub Images

| Image | URL |
|---|---|
| Backend | `vivvvekk/taskflow-backend:latest` |
| Frontend | `vivvvekk/taskflow-frontend:latest` |

---

## Environment Variables

| Variable | Required | Description | Example |
|---|---|---|---|
| `POSTGRES_DB` | Yes | Database name | `taskflow` |
| `POSTGRES_USER` | Yes | Database user | `taskflow_user` |
| `POSTGRES_PASSWORD` | **Yes — secret** | Database password | _(set in secret manager)_ |
| `DATABASE_URL` | Yes | Full PostgreSQL connection string | `postgresql://user:pass@postgres:5432/db` |
| `REDIS_URL` | Yes | Redis connection URL | `redis://redis:6379` |
| `JWT_SECRET` | **Yes — secret** | JWT signing secret | _(long random string)_ |
| `PORT` | No | Backend listen port (default `3000`) | `3000` |
| `DOCKERHUB_USERNAME` | Yes (deploy only) | Docker Hub username for image pull | `vivvvekk` |

---

## CI/CD Pipeline

### CD Workflow (`cd.yml`) — triggers on push to `main`

1. **Checkout** — pulls the student repo
2. **Validate secrets** — checks `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` exist
3. **Buildx setup** — multi-platform builder
4. **Docker Hub login** — authenticates with token
5. **Build & push backend** — `vivvvekk/taskflow-backend:latest`
6. **Build & push frontend** — `vivvvekk/taskflow-frontend:latest`
7. **Create .env** — injects deployment environment
8. **Validate deploy compose** — asserts no `build:` keys
9. **Pull images** — `docker compose -f docker-compose.deploy.yml pull`
10. **Deploy** — `docker compose -f docker-compose.deploy.yml up -d`
11. **Health check** — curls `http://localhost:3000/health`
12. **Frontend check** — curls `http://localhost:8080/`
13. **API tests** — runs `tests/` with Jest
14. **Cleanup** — `down -v`

### CI Workflow (`ci.yml`) — triggers on Pull Request to instructor's `main`

Same build/test flow but runs against the PR commit and uses instructor-controlled test scripts.

---

## GitHub Secrets Required

Go to: **Your Fork → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | `vivvvekk` |
| `DOCKERHUB_TOKEN` | _(your Docker Hub access token)_ |
| `POSTGRES_PASSWORD` | _(any strong password)_ |

---

## Persistence Verification

```bash
# 1. Add some tasks via the app at http://localhost:8080
# 2. Stop containers (WITHOUT -v to keep the volume)
docker compose down
# 3. Start again
docker compose up -d
# 4. Tasks survive — PostgreSQL data is in the named volume postgres_data
```

---

## Redis Caching Verification

```bash
# After loading tasks once, the second GET /api/tasks returns source: "redis-cache"
curl -H "Authorization: Bearer <token>" http://localhost:3000/api/tasks
# Check keys in Redis
docker compose exec redis redis-cli keys '*'
```
