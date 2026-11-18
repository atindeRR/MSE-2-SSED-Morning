# MSE-2 Morning Shift
# Software Engineering and DevOps (AI310B)
---

## 1. Problem Statement

You are provided with a fully functional full-stack web application.

The application consists of the following components:

- **Frontend:** React.js with Vite
- **Backend:** Node.js with Express.js
- **Database:** PostgreSQL
- **Caching:** Redis

Your task is to containerize the complete application using Docker and Docker Compose, publish the application images to your personal Docker Hub account, and verify the deployment through the provided GitHub Actions CI/CD pipelines.

You are required to implement the Docker-related configurations yourself. The application source code is already provided.

The objective is to demonstrate your understanding of containerization, Docker networking, persistent storage, image publishing, multi-container orchestration and automated CI/CD pipelines.

## 2. Repository Details

You will receive the starter repository .

Repository URL: https://github.com/atindeRR/MSE-2-SSED-Morning

You must complete the practical using your own GitHub and Dockerhub account.

### Initial Setup

1. Open the provided starter repository.
2. Fork the repository into your personal GitHub account.
3. Clone your forked repository to your local machine.

```bash
git clone https://github.com/YOUR_USERNAME/MSE-2-SSED-Morning.git
cd MSE-2-SSED-Morning
```

4. Explore the existing application structure and understand the frontend, backend, PostgreSQL and Redis dependencies.
5. Create a separate working branch (if required).

**Important:** Do not modify or remove the existing application functionality. Your task is to implement the containerization and deployment configurations.

---

## 3. Practical Tasks

### Task 1: Create Dockerfiles

Create separate Dockerfiles for the frontend and backend applications.

**Frontend Dockerfile**

Your frontend Dockerfile must:

- Use an appropriate base image.
- Install the required dependencies.
- Build the React application.
- Serve the production build using Nginx or an appropriate production web server.
- Expose the appropriate container port.
- Follow Docker best practices.

**Backend Dockerfile**

Your backend Dockerfile must:

- Use an appropriate Node.js base image.
- Install the required dependencies.
- Copy the application source code.
- Configure the application startup command.
- Expose the backend port.
- Use environment variables for application configuration.
- Follow Docker best practices.

**Expected Deliverables:**

```text
frontend/Dockerfile
backend/Dockerfile
```

### Task 2: Implement Docker Compose

Create a `docker-compose.yml` file to orchestrate all four application services.

Your Docker Compose configuration must include:

1. Frontend
2. Backend
3. PostgreSQL
4. Redis

**Requirements:**

- Configure all four services.
- Establish appropriate container networking.
- Configure environment variables.
- Configure service dependencies.
- Implement health checks wherever appropriate.
- Use Docker volumes for PostgreSQL data persistence.
- Ensure the backend communicates with PostgreSQL and Redis using service names rather than localhost.
- Ensure the frontend can communicate with the backend.
- Configure appropriate host-to-container port mappings.
- Ensure the complete application starts using a single Docker Compose command.

**Expected Deliverable:**

```text
docker-compose.yml
```

**Application Startup:**

```bash
docker compose up -d --build
```

Verify that all four containers are running successfully.

### Task 3: Docker Hub Image Publishing

Publish your frontend and backend Docker images to your personal Docker Hub account.

**Requirements:**

1. Create a Docker Hub account if you do not already have one.
2. Create two repositories:
   - `frontend`
   - `backend`
3. Build the frontend and backend images.
4. Tag the images using your Docker Hub username.
5. Push both images to Docker Hub.
6. Verify that the images are available in your Docker Hub repositories.

**Expected image naming convention:**

```text
YOUR_DOCKERHUB_USERNAME/frontend

YOUR_DOCKERHUB_USERNAME/backend
```

You may also publish a `latest` tag.

### Task 4: Deployment Using Published Images

Create a separate Docker Compose configuration named:

```text
docker-compose.deploy.yml
```

This configuration must deploy the application using the images published on Docker Hub.

**Requirements:**

- Use the published frontend and backend images.
- Do not use `build:` directives in this deployment configuration.
- Use PostgreSQL and Redis official images.
- Configure environment variables securely.
- Configure PostgreSQL persistent storage.
- Ensure the application can be deployed on a clean machine without rebuilding the frontend and backend images locally.

**Deployment Verification:**

```bash
docker compose -f docker-compose.deploy.yml pull

docker compose -f docker-compose.deploy.yml up -d
```

Verify that the application is accessible and functioning correctly.

---

## 4. CI/CD Pipeline Implementation and Verification

A GitHub Actions CI/CD workflow is provided as part of the starter repository.

You are required to configure and execute the provided pipeline.

### Step 1: Configure GitHub Secrets

Navigate to:

**GitHub → Your Fork → Settings → Secrets and variables → Actions**

Create the following repository secrets:

| Secret Name | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Your Docker Hub access token |
| `POSTGRES_PASSWORD` | Password for the PostgreSQL deployment |

Never commit credentials or access tokens directly into your repository.

### Step 2: Execute the CD Pipeline

Push your implementation to the `main` branch of your fork.

```bash
git add .

git commit -m "Implement Docker containerization and deployment"

git push origin main
```

The CD workflow should automatically execute.

Verify the following stages:

| CD Stage | Expected Result |
|---|---|
| Repository checkout | Successful |
| Docker Buildx setup | Successful |
| Docker Hub authentication | Successful |
| Backend image build | Successful |
| Backend image publishing | Successful |
| Frontend image build | Successful |
| Frontend image publishing | Successful |
| Docker Compose image pull | Successful |
| Application deployment | Successful |
| Backend health verification | Successful |
| Frontend accessibility verification | Successful |

### Step 3: Verify the CI/CD Results

Navigate to:

**GitHub → Your Fork → Actions**

Open the latest workflow execution.

Verify that all required stages have completed successfully.

You must ensure that:

- Both Docker images are published successfully.
- The published images can be pulled.
- The deployment Compose configuration works.
- All application services start successfully.
- The application health checks pass.

---

## 5. Final Submission Through Pull Request

After completing the implementation and verifying that the CD pipeline passes, prepare your final submission.

### Step 1: Commit the Latest Changes

Ensure that all final Docker-related configurations are committed and pushed to your fork.

```bash
git add .

git commit -m "Final Docker practical submission"

git push origin main
```

Verify that your latest changes are available in your GitHub fork.

### Step 2: Create a Pull Request

Navigate to your forked repository.

Select:

**Pull Requests → New Pull Request → Compare Across Forks**

Configure the Pull Request as follows:

| Field | Selection |
|---|---|
| Base Repository | Instructor's `taskflow-docker` repository |
| Base Branch | `main` |
| Head Repository | Your fork of `taskflow-docker` |
| Compare Branch | `main` |

Create the Pull Request.

**Pull Request Title Format:**

```text
DOCKER-EXAM | ROLL-NUMBER | STUDENT-NAME | SECTION
```

Example:

```text
DOCKER-EXAM | 230101 | Rahul Sharma | AIML-B
```

### Step 3: Include Submission Details

Your Pull Request description must contain:

```markdown
## Student Details

- Name:
- Roll Number:
- Section:
- GitHub Username:
- Docker Hub Username:

## Docker Hub Images

- Frontend Image:
- Backend Image:

## Application Deployment

- Application URL:
- Backend Health URL:

## Implementation Checklist

- [ ] Frontend Dockerfile implemented
- [ ] Backend Dockerfile implemented
- [ ] docker-compose.yml implemented
- [ ] docker-compose.deploy.yml implemented
- [ ] Frontend image published to Docker Hub
- [ ] Backend image published to Docker Hub
- [ ] PostgreSQL persistence verified
- [ ] Redis caching verified
- [ ] Application functionality tested
- [ ] CD pipeline passed successfully
- [ ] Latest changes committed and pushed

## CI/CD Verification

- CD Workflow Run URL:
- Final Workflow Status:

## Declaration

I confirm that the implementation submitted is my own work and that I have tested the containerized application.
```

### Step 4: Prepare and Submit PDF Documentation

Every student must prepare a PDF document containing the complete submission details and evidence of successful Docker implementation and CI/CD execution in moodle.

**PDF File Naming Convention:**

`ROLL_NUMBER_STUDENT_NAME.pdf`

**The PDF must contain the following information:**

#### 1. Student Information

- Full Name
- University Roll Number
- Section
- Branch
- GitHub Username

#### 2. GitHub Submission Details

- GitHub Repository URL (personal fork)
- GitHub branch used for the implementation

#### 3. Docker Hub Details

- Docker Hub Username
- Frontend Docker Image URL
- Backend Docker Image URL

#### 4. CI/CD Execution Evidence

Include clear screenshots demonstrating the successful execution of all CI/CD stages.

The screenshots must cover:

- GitHub Actions workflow execution.
- Docker Hub authentication.
- Backend Docker image build and publishing.
- Frontend Docker image build and publishing.
- Docker Compose image pull.
- Application deployment.
- Backend health check.
- Frontend accessibility verification.
- Final successful CI/CD pipeline status.
- Instructor CI evaluation results, if available.

#### 5. Declaration

Include the following declaration at the end of the PDF:

"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."

**Submission Instructions:**

1. Save the completed documentation as a PDF.
2. Attach the PDF to your final Pull Request.
3. Ensure that all screenshots are readable and clearly demonstrate successful execution.
4. Verify that all repository URLs and Docker Hub image URLs are accessible.

**Important:** Submission of the PDF documentation is mandatory. Incomplete documentation or missing CI/CD execution screenshots may result in deduction of marks.
---


## 6. Important Instructions

1. The application source code is provided. You are required to implement the Docker and deployment configurations.
2. Do not remove or alter existing application functionality to bypass evaluation.
3. Do not hardcode credentials, passwords or access tokens in Dockerfiles or Compose files.
4. Each student must use their own GitHub and Docker Hub accounts.
5. Docker Hub repositories must contain the images corresponding to the submitted application.
6. Your application must work using the published images, without relying on local frontend or backend builds.
7. Do not submit an incomplete or untested implementation.
8. The final Pull Request must contain your latest committed changes.
9. The instructor's CI evaluation must be allowed to execute against your Pull Request.
10. Be prepared to explain your Dockerfiles, networking, volumes, environment variables, image publishing and CI/CD workflow during the viva.

**Final Submission:** Your examination submission is considered complete only when your Docker implementation is pushed to your GitHub fork, the required CD stages have passed, and the final Pull Request has been created successfully.


---

# DevOps Implementation & Container Architecture Guide

## 1. Project Architecture

The application is a decoupled, modern multi-tier TaskFlow web application consisting of four dedicated container services running on an isolated bridge network (`taskflow-network`):

```
       [ Client Browser ]
               │
        Port 8080 (Host)
               ▼
┌───────────────────────────────────────────────┐
│              Frontend Container               │
│        (Nginx 1.27-Alpine Web Server)         │
│  - Serves compiled React/Vite SPA on Port 80  │
│  - Reverse proxies /api/ -> backend:3000/api/ │
│  - Reverse proxies /health -> backend:3000    │
└───────────────────────┬───────────────────────┘
                        │
                  Docker Network
              (http://backend:3000)
                        ▼
┌───────────────────────────────────────────────┐
│               Backend Container               │
│             (Node.js 20-Alpine)               │
│  - Express REST API listening on Port 3000    │
│  - Health endpoint: /health                   │
│  - Non-root user execution (UID 1000)         │
└───┬───────────────────────────────────────┬───┘
    │                                       │
    │ PostgreSQL Protocol                   │ Redis Protocol
    │ (postgres:5432)                       │ (redis:6379)
    ▼                                       ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│   PostgreSQL Container  │   │     Redis Container     │
│   (postgres:16-alpine)  │   │     (redis:7-alpine)    │
│ - Named volume storage  │   │ - In-memory key caching │
│ - Auto schema init      │   │ - Health check via ping │
└─────────────────────────┘   └─────────────────────────┘
```

### Communication Flow:
1. **Frontend to Backend**: The browser connects to `http://localhost:8080`. Static assets are served directly by Nginx. All `/api/*` and `/health` requests are reverse-proxied internally to `http://backend:3000` via Docker's DNS resolution.
2. **Backend to Database**: Backend connects to PostgreSQL via the connection string `postgresql://taskflow_user:${POSTGRES_PASSWORD}@postgres:5432/taskflow`. The hostname `postgres` is resolved via Docker internal DNS.
3. **Backend to Cache**: Backend connects to Redis via `redis://redis:6379`. The hostname `redis` is resolved via Docker internal DNS.

---

## 2. Explanation of All Four Containers

### 1. Frontend (`frontend/Dockerfile`)
- **Base Images**: `node:20-alpine` (builder) and `nginx:1.27-alpine` (production).
- **Multi-Stage Build**:
  - *Builder Stage*: Installs dependencies from lockfile (`npm ci`), copies source code, and builds optimized production assets using Vite.
  - *Production Stage*: Copies compiled assets (`dist/`) into `/usr/share/nginx/html` and mounts custom `nginx.conf` into `/etc/nginx/conf.d/default.conf`.
- **Port**: Container port 80 mapped to host port 8080.
- **Routing & Reverse Proxy**: Configured for SPA fallback (`try_files $uri $uri/ /index.html;`) and reverse proxying for `/api/` and `/health`.
- **Healthcheck**: Periodically verifies Nginx server availability via `wget`.

### 2. Backend (`backend/Dockerfile`)
- **Base Image**: `node:20-alpine`.
- **Security & Best Practices**: Runs under non-root user `USER 1000`, uses cached dependency installation (`npm ci --omit=dev`), and cleans npm cache.
- **Port**: Container port 3000 mapped to host port 3000.
- **Environment**: Configured with production defaults (`NODE_ENV=production`, `PORT=3000`).
- **Healthcheck**: Uses `wget` to query `http://127.0.0.1:3000/health`.

### 3. PostgreSQL Database (`postgres`)
- **Image**: `postgres:16-alpine`.
- **Data Persistence**: Uses named Docker volume `postgres_data` mapped to `/var/lib/postgresql/data`.
- **Schema Initialization**: Mounts `backend/db/init.sql` to `/docker-entrypoint-initdb.d/init.sql:ro` for automatic schema creation on initial startup.
- **Healthcheck**: Uses `pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}`.

### 4. Redis Cache (`redis`)
- **Image**: `redis:7-alpine`.
- **Role**: Caches task lists (`tasks:user:${userId}`) for 30 seconds and invalidates cache upon task mutations.
- **Healthcheck**: Uses `redis-cli ping`.

---

## 3. Environment Variables & Security Management

All configuration is managed via environment variables. Never commit `.env` to source control.

Copy `.env.example` to create `.env`:
```bash
cp .env.example .env
```

### Environment Variable Reference:

| Variable | Description | Example / Default |
|---|---|---|
| `DOCKERHUB_USERNAME` | Your personal Docker Hub username | `ItsmeYuvi` |
| `POSTGRES_DB` | Name of PostgreSQL database | `taskflow` |
| `POSTGRES_USER` | PostgreSQL master username | `taskflow_user` |
| `POSTGRES_PASSWORD` | PostgreSQL master password | *Secure custom password* |
| `DATABASE_URL` | Full backend database connection string | `postgresql://taskflow_user:<password>@postgres:5432/taskflow` |
| `REDIS_URL` | Full Redis connection string | `redis://redis:6379` |
| `JWT_SECRET` | Secret key for signing JWT tokens | *Long random secret string* |
| `PORT` | Backend application listening port | `3000` |

---

## 4. Local Startup & Verification Commands

### Start All Services (Build from Source):
```bash
docker compose up -d --build
```

### Verify Running Containers and Health Status:
```bash
docker compose ps
```

### Inspect Container Logs:
```bash
docker compose logs -f
```

### Verify Endpoints:
```bash
# Backend health directly
curl http://localhost:3000/health

# Frontend reverse-proxied health
curl http://localhost:8080/health

# Frontend application UI
curl -I http://localhost:8080/
```

### Run Test Suite:
```bash
cd tests
npm install
npm test
cd ..
```

### Stop All Services:
```bash
docker compose down
```

---

## 5. Deployment Using Published Images (`docker-compose.deploy.yml`)

The production deployment configuration uses exclusively pre-published Docker Hub images without any `build:` directives.

### Pull Published Images:
```bash
docker compose -f docker-compose.deploy.yml pull
```

### Launch Deployment Stack:
```bash
docker compose -f docker-compose.deploy.yml up -d
```

### Verify Deployment:
```bash
docker compose -f docker-compose.deploy.yml ps
curl http://localhost:3000/health
curl -I http://localhost:8080/
```

### Teardown Deployment:
```bash
docker compose -f docker-compose.deploy.yml down
```

---

## 6. Docker Hub Image Publishing Instructions

### Manual Build, Tag & Push via CLI:
```bash
# Set your Docker Hub username
export DOCKERHUB_USERNAME=YOUR_DOCKERHUB_USERNAME

# Authenticate to Docker Hub
docker login -u "$DOCKERHUB_USERNAME"

# Build and tag backend
docker build -t "$DOCKERHUB_USERNAME/taskflow-backend:latest" -t "$DOCKERHUB_USERNAME/backend:latest" ./backend

# Build and tag frontend
docker build -t "$DOCKERHUB_USERNAME/taskflow-frontend:latest" -t "$DOCKERHUB_USERNAME/frontend:latest" ./frontend

# Push backend images
docker push "$DOCKERHUB_USERNAME/taskflow-backend:latest"
docker push "$DOCKERHUB_USERNAME/backend:latest"

# Push frontend images
docker push "$DOCKERHUB_USERNAME/taskflow-frontend:latest"
docker push "$DOCKERHUB_USERNAME/frontend:latest"
```

---

## 7. GitHub Actions CI/CD Pipeline & Secrets Setup

### Required Secrets:
In your GitHub personal fork, navigate to **Settings → Secrets and variables → Actions** and add:
1. `DOCKERHUB_USERNAME`: Your Docker Hub username.
2. `DOCKERHUB_TOKEN`: Your Docker Hub Personal Access Token (PAT) with `Read, Write, Delete` permissions.
3. `POSTGRES_PASSWORD`: Secure password for the PostgreSQL container deployment.

### Pipeline Workflow Summary:
- **`ci.yml` (Triggered on Pull Requests)**:
  - Validates `frontend/Dockerfile` and `backend/Dockerfile` with Hadolint.
  - Generates CI environment and builds containers with `docker compose build`.
  - Spins up stack and waits for healthy backend and frontend status.
  - Runs 12 automated API and cache tests via Jest.
  - Verifies PostgreSQL persistent storage across container restarts.
- **`cd.yml` (Triggered on push to `main`)**:
  - Authenticates to Docker Hub securely via secrets.
  - Builds and tags frontend and backend images with `latest` and commit SHA (`${{ github.sha }}`).
  - Pushes both images to Docker Hub.
  - Pulls published images using `docker-compose.deploy.yml`.
  - Deploys the stack and verifies health endpoints and API test suite.

---

## 8. Verification & Application URLs

- **Frontend Application**: `http://localhost:8080/`
- **Backend API Health**: `http://localhost:3000/health`
- **Nginx Proxied Health**: `http://localhost:8080/health`
- **Expected Health Response**:
  ```json
  {"status":"ok","postgres":"ok","redis":"ok"}
  ```

---

## 9. Troubleshooting Guide

| Issue | Cause | Resolution |
|---|---|---|
| `port is already allocated (3000 or 8080)` | Another container or process is listening on the host port. | Run `docker ps` and `docker stop <container_id>` or check host processes via `netstat -ano`. |
| Backend waits for PostgreSQL indefinitely | PostgreSQL container not healthy or incorrect credentials. | Check `docker compose logs postgres` and verify `DATABASE_URL` matches `POSTGRES_USER` and `POSTGRES_PASSWORD`. |
| `docker compose config` reports empty variable | Missing `.env` file. | Ensure `.env` is created from `.env.example` in the project root. |
| Hadolint warning DL3066 on Dockerfile | Non-numeric user ID used. | Use `USER 1000` rather than `USER node`. |
| Jest tests fail with `ECONNREFUSED` | Containers not fully started before test execution. | Ensure `docker compose ps` shows all containers in `(healthy)` state. |
