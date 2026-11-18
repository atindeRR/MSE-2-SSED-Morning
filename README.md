# TaskFlow - Containerized DevOps Exam Implementation

## 1. Project Introduction

**TaskFlow** is a modern full-stack web application designed for personal task management. The application provides user authentication (registration and login via JWT tokens) and a complete CRUD task management interface with status tracking (`Pending`, `In Progress`, `Completed`). 

This project delivers the complete containerization, orchestration, Docker Hub publishing, and CI/CD automation for the TaskFlow platform as required by the **MSE-2 Software Engineering and DevOps Practical Examination**.

---

## 2. Technology Stack

- **Frontend:** React.js 18, Vite 5, Nginx 1.27 (Production Web Server & Reverse Proxy)
- **Backend:** Node.js 20 (LTS), Express.js 4, PostgreSQL Driver (`pg` 8.13), Redis Client (`redis` 4.7), JSON Web Tokens (`jsonwebtoken`), Password Hashing (`bcryptjs`)
- **Database:** PostgreSQL 16 (Relational persistent storage)
- **Cache:** Redis 7.4 (In-memory caching and session acceleration)
- **Containerization & Orchestration:** Docker Engine, Docker Compose v2, Docker Buildx
- **CI/CD:** GitHub Actions (Automated Hadolint linting, image build, image publishing, compose validation, integration testing)
- **Testing:** Jest 29, Supertest 7

---

## 3. Repository Structure

```text
MSE_2/
├── .github/
│   └── workflows/
│       ├── ci.yml                 # PR evaluation: Hadolint, Compose test, Jest API tests, Persistence test
│       └── cd.yml                 # Push CD pipeline: Docker Hub auth, build & push, deploy verification
├── backend/
│   ├── db/
│   │   └── init.sql               # PostgreSQL database schema (users & tasks tables, indexes)
│   ├── src/
│   │   ├── app.js                 # Express application routing, auth endpoints, CRUD task routes, cache logic
│   │   ├── auth.js                # JWT verification middleware
│   │   ├── config.js              # Environment variable parsing and fallback configuration
│   │   ├── db.js                  # PostgreSQL pg.Pool connection and retry logic
│   │   ├── redis.js               # Redis client connection and retry logic
│   │   └── server.js              # HTTP server bootstrapper and graceful shutdown handlers
│   ├── .dockerignore              # Excludes node_modules, .env, git history, test files from Docker context
│   ├── Dockerfile                 # Pinned Node.js 20 Alpine production image with non-root user
│   └── package.json               # Backend dependencies and startup scripts
├── frontend/
│   ├── src/
│   │   ├── main.jsx               # React UI root component (Task management, Auth modal, cache indicator)
│   │   └── style.css              # Custom styling
│   ├── .dockerignore              # Excludes node_modules, dist, .env from frontend Docker context
│   ├── Dockerfile                 # Multi-stage Dockerfile (Node.js build stage -> Nginx 1.27 Alpine runtime)
│   ├── index.html                 # Single Page Application HTML template
│   ├── nginx.conf                 # Nginx server configuration (SPA routing fallback and API proxy)
│   ├── package.json               # Frontend dependencies and Vite build scripts
│   └── vite.config.js             # Vite configuration with React plugin
├── tests/
│   ├── api.test.js                # 12 automated integration tests for health, auth, tasks, Redis caching
│   ├── jest.config.js             # Jest test configuration
│   ├── package.json               # Test dependencies (jest, supertest)
│   └── package-lock.json          # Pinned test dependency lockfile
├── .env.example                   # Template environment variables with placeholders
├── .gitignore                     # Git ignore rules for node_modules, local .env, build output
├── docker-compose.yml             # Orchestration for all 4 services with local build configuration
├── docker-compose.deploy.yml      # Deployment orchestration using published Docker Hub images (no build)
├── submission.json                # Student exam submission identity file
└── README.md                      # Comprehensive project and operational documentation
```

---

## 4. Docker Architecture

The TaskFlow application is designed with a microservices-inspired architecture:

```
                            +----------------------------------------+
                            |              Host Machine              |
                            +----------------------------------------+
                                  |                             |
                       Port 8080  |                  Port 3000  |
                                  v                             v
                   +----------------------------+  +----------------------------+
                   |     taskflow-frontend      |  |      taskflow-backend      |
                   |       (Nginx 1.27)         |  |      (Node.js 20 LTS)      |
                   |   Internal Port: 80/tcp    |  |   Internal Port: 3000/tcp  |
                   +----------------------------+  +----------------------------+
                     | Proxy: /api/* -> backend:3000   |                    |
                     | Proxy: /health -> backend:3000  |                    |
                     +---------------------------------+                    |
                                                       |                    |
                                                       v                    v
                                          +------------------+  +------------------+
                                          | taskflow-postgres|  |  taskflow-redis  |
                                          | (PostgreSQL 16)  |  |   (Redis 7.4)    |
                                          | Port: 5432/tcp   |  |  Port: 6379/tcp  |
                                          +------------------+  +------------------+
                                                   |
                                                   v
                                          +------------------+
                                          |  postgres_data   |
                                          |  (Named Volume)  |
                                          +------------------+
```

### Communication Flow:
1. **User Client** accesses `http://localhost:8080/` to retrieve the React Single Page Application served by Nginx.
2. When the user interacts with the UI, requests to `/api/*` and `/health` are routed directly to Nginx on port 8080.
3. **Nginx Reverse Proxy** forwards these requests internally to `http://backend:3000/` across the isolated Docker network `taskflow-network`.
4. **Backend** communicates with **PostgreSQL** on `postgres:5432` for persistent data and with **Redis** on `redis:6379` for caching.
5. All 4 containers communicate securely through hostnames provided by Docker's built-in DNS service discovery.

---

## 5. Dockerfile Explanations

### 5.1 Frontend Dockerfile (`frontend/Dockerfile`)
The frontend uses a **multi-stage build** adhering strictly to Hadolint linting and production security practices:

- **Stage 1: Build Stage (`node:20.18.1-alpine3.20 AS builder`)**
  - Uses an exact pinned version of Alpine Node.js.
  - Sets `WORKDIR /app`.
  - Copies `package*.json` separately before application code to leverage Docker cache layers.
  - Installs build tools and dependencies via `npm install`.
  - Copies frontend source code and compiles the production bundle using `npm run build` (outputs to `/app/dist`).
- **Stage 2: Production Stage (`nginx:1.27.2-alpine`)**
  - Uses an exact pinned version of Nginx Alpine.
  - Copies only the compiled static assets (`/app/dist`) to `/usr/share/nginx/html`.
  - Copies `nginx.conf` to `/etc/nginx/conf.d/default.conf` to enable SPA fallback (`try_files $uri $uri/ /index.html;`) and reverse proxy `/api/` and `/health` to `http://backend:3000/`.
  - Exposes port 80.
  - Contains **zero** Node.js runtime or `node_modules` in the final image, drastically reducing attack surface and image size.

### 5.2 Backend Dockerfile (`backend/Dockerfile`)
The backend is packaged into a secure, minimal production container:

- Uses pinned `node:20.18.1-alpine3.20`.
- Sets `WORKDIR /app` and defines `NODE_ENV=production` and `PORT=3000`.
- Copies `package*.json` first and executes `npm install --omit=dev && npm cache clean --force` to install only required production dependencies (`express`, `pg`, `redis`, `bcryptjs`, `jsonwebtoken`, `cors`).
- Copies source code (`src/`) and SQL schema (`db/`) with non-root ownership (`COPY --chown=1000:1000`).
- Adheres to security best practices by running as a non-privileged user `USER 1000:1000` (Node user).
- Exposes port 3000.
- Starts using `CMD ["npm", "start"]` which invokes `node src/server.js`.
- Contains **no hardcoded credentials**; configuration is dynamically read from environment variables.

---

## 6. Docker Compose Service Descriptions

`docker-compose.yml` configures exactly four interdependent services:

1. **`postgres`**:
   - Image: `postgres:16-alpine`
   - Volume: Named volume `postgres_data` mounted at `/var/lib/postgresql/data`.
   - Initialization: `./backend/db/init.sql` mounted read-only at `/docker-entrypoint-initdb.d/init.sql:ro`.
   - Healthcheck: `pg_isready -U ${POSTGRES_USER:-taskflow_user} -d ${POSTGRES_DB:-taskflow}`.
   - Restart: `unless-stopped`.

2. **`redis`**:
   - Image: `redis:7.4-alpine`
   - Healthcheck: `redis-cli ping`.
   - Restart: `unless-stopped`.

3. **`backend`**:
   - Build: Context `./backend`, Dockerfile `Dockerfile`.
   - Depends On: `postgres` (`condition: service_healthy`), `redis` (`condition: service_healthy`).
   - Ports: `3000:3000`.
   - Healthcheck: `wget -qO- http://127.0.0.1:3000/health || exit 1`.
   - Environment: Reads database and Redis URLs pointing to service hostnames `postgres` and `redis`.
   - Restart: `unless-stopped`.

4. **`frontend`**:
   - Build: Context `./frontend`, Dockerfile `Dockerfile`.
   - Depends On: `backend` (`condition: service_healthy`).
   - Ports: `8080:80` (Host port 8080 mapped to container port 80).
   - Healthcheck: `wget -qO- http://127.0.0.1:80/ > /dev/null || exit 1`.
   - Restart: `unless-stopped`.

---

## 7. Network Configuration

- **Network Name:** `taskflow-network`
- **Driver:** `bridge`
- **DNS Discovery:** Containers address each other by their service names (`postgres`, `redis`, `backend`, `frontend`) rather than IP addresses or `localhost`.
- **Isolation:** Database and cache ports (5432 and 6379) are kept internal to the Docker network and are not exposed directly to the host machine, preventing unauthorized host access.

---

## 8. PostgreSQL Volume Persistence

- **Volume Name:** `taskflow_postgres_data` (`postgres_data`)
- **Mount Path:** `/var/lib/postgresql/data`
- **Behavior:** PostgreSQL stores database files on this managed Docker volume. Even when containers are stopped (`docker compose down`) or updated, the volume remains intact. Data is only wiped if explicitly requested using `docker compose down -v`.

---

## 9. Redis Configuration

- **Service Name:** `redis`
- **Image:** `redis:7.4-alpine`
- **Integration in Backend:**
  - Tasks list (`GET /api/tasks`) is cached in Redis under the key `tasks:user:<userId>` with a 30-second Time-To-Live (TTL).
  - Cache is immediately invalidated (`redis.del`) upon task creation (`POST /api/tasks`), task update (`PATCH /api/tasks/:id`), or task deletion (`DELETE /api/tasks/:id`).
  - Health check endpoint `/health` validates connectivity by issuing `redis.ping()`.

---

## 10. Environment Variables

The project uses `.env` for runtime secrets and configuration. A `.env.example` file is provided with safe placeholder values:

| Variable | Description | Default / Example Value |
|---|---|---|
| `POSTGRES_DB` | PostgreSQL database name | `taskflow` |
| `POSTGRES_USER` | PostgreSQL username | `taskflow_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `your_secure_postgres_password` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://taskflow_user:...@postgres:5432/taskflow` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `PORT` | Backend listening port | `3000` |
| `JWT_SECRET` | Secret key for JWT signing | `your_jwt_secret_key_minimum_32_characters` |
| `DOCKERHUB_USERNAME` | Docker Hub username | `your_dockerhub_username` |

---

## 11. Local Setup Instructions

### Prerequisites
- Docker Engine 24+ and Docker Compose v2 installed and running.

### Quick Start (Single Command)
1. Clone your repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MSE-2-SSED-Morning.git
   cd MSE-2-SSED-Morning
   ```

2. Create `.env` from template:
   ```bash
   cp .env.example .env
   ```

3. Launch the complete containerized stack:
   ```bash
   docker compose up -d --build
   ```

4. Verify container status:
   ```bash
   docker compose ps
   ```

5. Access the application:
   - **Frontend UI:** [http://localhost:8080/](http://localhost:8080/)
   - **Backend Health Check:** [http://localhost:3000/health](http://localhost:3000/health)

6. Run integration tests:
   ```bash
   cd tests
   npm install
   npx jest --runInBand
   ```

7. Stop the stack:
   ```bash
   docker compose down
   ```

---

## 12. Docker Hub Publishing Commands

To build, tag, and publish the images to your Docker Hub account:

```bash
# 1. Login to Docker Hub
docker login

# 2. Build and tag the frontend image
docker build -t YOUR_DOCKERHUB_USERNAME/frontend:latest ./frontend
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest ./frontend

# 3. Build and tag the backend image
docker build -t YOUR_DOCKERHUB_USERNAME/backend:latest ./backend
docker build -t YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest ./backend

# 4. Push images to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/frontend:latest
docker push YOUR_DOCKERHUB_USERNAME/taskflow-frontend:latest
docker push YOUR_DOCKERHUB_USERNAME/backend:latest
docker push YOUR_DOCKERHUB_USERNAME/taskflow-backend:latest
```

---

## 13. Deployment Instructions

To deploy the application on any clean machine using published Docker Hub images without compiling local source:

1. Copy `docker-compose.deploy.yml` and `.env` to the target machine.
2. In `.env`, ensure `DOCKERHUB_USERNAME` is set to your Docker Hub username.
3. Pull the published images:
   ```bash
   docker compose -f docker-compose.deploy.yml pull
   ```
4. Start the stack:
   ```bash
   docker compose -f docker-compose.deploy.yml up -d
   ```
5. Verify container health:
   ```bash
   docker compose -f docker-compose.deploy.yml ps
   curl http://localhost:3000/health
   curl http://localhost:8080/
   ```

---

## 14. GitHub Actions Configuration

The repository includes automated CI and CD workflows under `.github/workflows/`:

### Required Repository Secrets
Navigate to **GitHub → Your Fork → Settings → Secrets and variables → Actions** and add:
- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: Your Docker Hub Personal Access Token (Read/Write/Delete permissions).
- `POSTGRES_PASSWORD`: The database password for deployment.

### Pipeline Highlights:
- **`ci.yml` (Pull Request Evaluation):**
  - Lints `frontend/Dockerfile` and `backend/Dockerfile` with Hadolint.
  - Builds and starts the complete multi-container stack.
  - Confirms backend health and frontend availability.
  - Executes the 12 Jest API/Redis integration tests.
  - Validates PostgreSQL volume data persistence across container restarts.
- **`cd.yml` (Publish & Deployment Verification):**
  - Authenticates to Docker Hub via repository secrets.
  - Builds and pushes frontend and backend images tagged with `latest` and commit SHA.
  - Validates `docker-compose.deploy.yml` (ensures zero `build:` directives).
  - Pulls images and deploys the stack.
  - Runs end-to-end integration tests against the live deployment.

---

## 15. Troubleshooting Commands

- **Check container logs:**
  ```bash
  docker compose logs -f backend
  docker compose logs -f frontend
  docker compose logs -f postgres
  docker compose logs -f redis
  ```
- **Inspect container health:**
  ```bash
  docker inspect --format='{{json .State.Health}}' taskflow-backend
  ```
- **Verify database connectivity:**
  ```bash
  docker exec -it taskflow-postgres psql -U taskflow_user -d taskflow -c "\dt"
  ```
- **Inspect Redis keys:**
  ```bash
  docker exec -it taskflow-redis redis-cli keys "*"
  ```
- **Test Hadolint locally:**
  ```bash
  docker run --rm -i hadolint/hadolint < frontend/Dockerfile
  docker run --rm -i hadolint/hadolint < backend/Dockerfile
  ```
- **Tear down stack and wipe volumes:**
  ```bash
  docker compose down -v --remove-orphans
  ```
