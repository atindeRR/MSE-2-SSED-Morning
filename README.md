# TaskFlow - MSE-2 Practical Containerization and Deployment

## 1. Project Overview & Architecture

TaskFlow is a production-grade multi-tier web application designed to demonstrate containerization, isolated networking, persistent storage, and automated CI/CD pipelines.

### Architecture Components
- **Frontend**: Single Page Application built with React and Vite. In production, static assets are served through an unprivileged Nginx reverse proxy running on port `80` (mapped to host port `8080`). Nginx proxies API calls (`/api/` and `/health`) directly to the backend service.
- **Backend API**: RESTful service built with Node.js and Express. It connects to PostgreSQL for relational persistence and Redis for caching and session state. Listens on port `3000` (mapped to host port `3000`).
- **Database (PostgreSQL)**: PostgreSQL 15 Alpine storing users and tasks. Data persists via a named Docker volume (`taskflow-postgres-data`). The initialization schema is auto-loaded via `/docker-entrypoint-initdb.d/init.sql`.
- **Caching (Redis)**: Redis 7 Alpine caching task lists with TTL and invalidation on task mutations (create, update, delete).

```text
  [ User Browser ]
         │
         │ (HTTP :8080)
         ▼
  [ Frontend Service (Nginx) ]
         │
         │ (Internal Proxy http://backend:3000)
         ▼
  [ Backend Service (Express API :3000) ]
         │                    │
         │ (Port 5432)        │ (Port 6379)
         ▼                    ▼
  [ PostgreSQL DB ]     [ Redis Cache ]
  (Named Volume)
```

---

## 2. Docker Files Explanation

### `frontend/Dockerfile`
- **Multi-Stage Build**:
  - **Stage 1 (Builder)**: Uses `node:20-alpine` to install dependencies via `npm install` and compile production assets with `npm run build`.
  - **Stage 2 (Runtime)**: Uses the secure `nginxinc/nginx-unprivileged:alpine-slim` image, running as an unprivileged user. It copies `frontend/nginx.conf` and compiled static files from `/app/dist` to `/usr/share/nginx/html`.
- **Port**: Exposes port `80`.

### `backend/Dockerfile`
- **Multi-Stage Build**:
  - **Stage 1 (Dependencies)**: Uses `node:20-alpine` to install production dependencies (`npm install --omit=dev`) and clears npm cache.
  - **Stage 2 (Runtime)**: Copies production `node_modules` and application source (`src/`). Runs under the non-root `node` user for security.
- **Port**: Exposes port `3000`.
- **Startup**: Executes `node src/server.js`.

### `.dockerignore` Files
- Both `frontend/.dockerignore` and `backend/.dockerignore` prevent leaking local build artifacts, `node_modules`, secret files (`.env`), and Git metadata into images, keeping build contexts fast and minimal.

### `docker-compose.yml`
Local development and CI orchestration file configuring:
- `frontend`: Builds from `./frontend`, maps host `8080:80`.
- `backend`: Builds from `./backend`, maps host `3000:3000`.
- `postgres`: PostgreSQL 15, maps `5432:5432`, persists data to `taskflow-postgres-data`, seeds with `./backend/db/init.sql`.
- `redis`: Redis 7, maps `6379:6379`.
- **Service Discovery**: Services communicate over the custom bridge network `taskflow-network` via service hostnames (`backend`, `postgres`, `redis`).
- **Health Checks & Dependencies**: Backend starts only after Postgres and Redis report healthy; frontend starts after backend is healthy.

### `docker-compose.deploy.yml`
Pure production deployment orchestration file:
- Pulls published images from Docker Hub (`${DOCKERHUB_USERNAME}/taskflow-backend:latest` and `${DOCKERHUB_USERNAME}/taskflow-frontend:latest`).
- Contains **no `build:` directives**, allowing zero-source deployment on clean servers.
- Connects to official `postgres:15-alpine` and `redis:7-alpine` images with persistent volume storage.

---

## 3. Local Build & Run Instructions

### Prerequisites
- Docker and Docker Compose (or Docker Desktop) installed.
- Git.

### 1. Configure Local Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Ensure `.env` contains:
```env
POSTGRES_DB=taskflow
POSTGRES_USER=taskflow_user
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://taskflow_user:your_secure_password@postgres:5432/taskflow
REDIS_URL=redis://redis:6379
JWT_SECRET=your_jwt_secret_key_here
PORT=3000
```

### 2. Build and Start the Stack
```bash
docker compose up -d --build
```

### 3. Check Service Status and Logs
```bash
docker compose ps
docker compose logs -f
```

### 4. Verify Access
- **Frontend UI**: [http://localhost:8080](http://localhost:8080)
- **Backend Health Check**: [http://localhost:3000/health](http://localhost:3000/health) (or via frontend proxy: [http://localhost:8080/health](http://localhost:8080/health))

### 5. Tear Down Stack
```bash
docker compose down -v
```

---

## 4. Manual Docker Hub Build, Tag & Push

If building and pushing manually to Docker Hub:

```bash
# 1. Login to Docker Hub
docker login

# 2. Build and tag backend image
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest ./backend

# 3. Build and tag frontend image
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest ./frontend

# 4. Push images to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest
docker push YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest
```

---

## 5. Deployment Using Published Images (`docker-compose.deploy.yml`)

Deploy on any machine with only Docker installed (no source code required):

```bash
# 1. Provide deployment environment variables
export DOCKERHUB_USERNAME="YOUR_DOCKERHUB_USERNAME"
export POSTGRES_PASSWORD="your_secure_password"
export JWT_SECRET="your_production_secret"
# Or put them into a local .env file

# 2. Pull the published images from Docker Hub
docker compose -f docker-compose.deploy.yml pull

# 3. Launch the deployment stack
docker compose -f docker-compose.deploy.yml up -d

# 4. Verify health
curl -f http://localhost:3000/health
curl -f http://localhost:8080/
```

To stop the deployment stack:
```bash
docker compose -f docker-compose.deploy.yml down
```

---

## 6. GitHub Repository Secrets Required

To enable the automated GitHub Actions CI/CD workflows (`.github/workflows/cd.yml` and `.github/workflows/ci.yml`), configure the following secrets in **GitHub → Repository Settings → Secrets and variables → Actions**:

| Secret Name | Description | Example |
|---|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub account username | `johndoe` |
| `DOCKERHUB_TOKEN` | Docker Hub Personal Access Token (Read & Write permissions) | `dckr_pat_...` |
| `POSTGRES_PASSWORD` | Password used for PostgreSQL during deployment | `strong_db_password_123` |

---

## 7. Verification and Testing

### Run Integration Tests
With the stack running (locally or in CI):
```bash
cd tests
npm install
npm test
```
The test suite validates:
1. Health endpoint (`/health`) confirming API, PostgreSQL, and Redis connectivity.
2. User registration and rejection of duplicate emails.
3. User login and JWT token issuance.
4. Protected route authentication.
5. Task creation, caching in Redis, updates, status validation, cache invalidation, and deletion.

---

## 8. Troubleshooting

- **Backend cannot connect to PostgreSQL**:
  Ensure PostgreSQL container is healthy (`docker compose ps`). Check that `DATABASE_URL` uses the hostname `postgres` and matches `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`.
- **Backend cannot connect to Redis**:
  Ensure Redis is running and reachable at `redis://redis:6379`.
- **Frontend shows 502 Bad Gateway on API calls**:
  Verify backend container is running on port 3000 and connected to `taskflow-network`. Inspect Nginx logs: `docker compose logs frontend`.
- **Permission errors on Docker commands**:
  Ensure Docker daemon is running and user has Docker permissions.
- **Docker Compose deploy fails to pull images**:
  Ensure `DOCKERHUB_USERNAME` is exported or defined in `.env` and repositories on Docker Hub are public or logged in via `docker login`.
