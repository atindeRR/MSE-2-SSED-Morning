# MSE-2 PRACTICAL EXAMINATION SUBMISSION DOCUMENTATION
## Course: Software Engineering and DevOps (AI310B)

---

### 1. Student Information
- **Full Name:** Adarsh Kumar
- **University Roll Number:** 202401100300012
- **Section:** CSE AI-A
- **Branch:** Computer Science & Engineering (AI)
- **GitHub Username:** adarsh165787

---

### 2. GitHub Submission Details
- **GitHub Repository URL (Personal Fork):** `https://github.com/adarsh165787/MSE-2-SSED-Morning`
- **Target Instructor Repository:** `https://github.com/atindeRR/MSE-2-SSED-Morning`
- **Working / Submission Branch:** `main`
- **Pull Request Title:** `DOCKER-EXAM | 202401100300012 | Adarsh Kumar | CSE AI-A`

---

### 3. Docker Hub Details
- **Docker Hub Username:** `adarsh165787`
- **Frontend Docker Image URL:** `https://hub.docker.com/r/adarsh165787/frontend` (and `taskflow-frontend`)
- **Backend Docker Image URL:** `https://hub.docker.com/r/adarsh165787/backend` (and `taskflow-backend`)

---

### 4. Docker Architecture Overview
The application consists of four distinct containerized services connected via a dedicated bridge network (`taskflow-network`):
1. **Frontend:** React + Vite Single Page Application served by Nginx 1.27 on port 80 (mapped to host 8080).
2. **Backend:** Node.js 20 Express REST API listening on port 3000.
3. **Database:** PostgreSQL 16 Alpine with named volume persistence (`postgres_data`).
4. **Caching:** Redis 7.4 Alpine for in-memory caching of task queries.

Nginx acts as a reverse proxy, forwarding `/api/*` and `/health` requests directly to `http://backend:3000/`.

---

### 5. Docker Implementation Details

#### 5.1 Frontend Dockerfile (`frontend/Dockerfile`)
- Multi-stage build pattern:
  - Stage 1: `node:20.18.1-alpine3.20` builds the Vite production bundle.
  - Stage 2: `nginx:1.27.2-alpine` serves static files and handles SPA routing fallback.
- No Node.js runtime or `node_modules` present in final production image.
- Passes Hadolint linting with zero warnings/errors.

#### 5.2 Backend Dockerfile (`backend/Dockerfile`)
- Base image: `node:20.18.1-alpine3.20`.
- Dependency installation: Layer-cached `npm install --omit=dev`.
- Security: Non-root execution using `USER 1000:1000`.
- Passes Hadolint linting with zero warnings/errors.

#### 5.3 Docker Compose (`docker-compose.yml` & `docker-compose.deploy.yml`)
- All 4 services defined with health checks, restart policies, and network isolation.
- Named volume `taskflow_postgres_data` ensures data persists across restarts.
- `docker-compose.deploy.yml` utilizes published Docker Hub images with zero `build:` directives.

---

### 6. Local Testing and Verification Evidence

#### Screenshot 1: Backend Health Check (`/health`)
*(Capture `curl http://localhost:3000/health` returning `{"status":"ok","postgres":"ok","redis":"ok"}`)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                        [INSERT SCREENSHOT: BACKEND HEALTH]                      |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

#### Screenshot 2: Frontend Accessibility (`http://localhost:8080/`)
*(Capture web browser loading the TaskFlow UI or curl returning index.html)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                    [INSERT SCREENSHOT: FRONTEND ACCESSIBILITY]                  |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

#### Screenshot 3: Running Containers (`docker compose ps`)
*(Capture all 4 containers healthy in terminal / Docker Desktop)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                     [INSERT SCREENSHOT: DOCKER COMPOSE PS]                      |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

---

### 7. Docker Hub Publishing Evidence

#### Screenshot 4: Docker Hub Frontend Repository
*(Capture Docker Hub web page showing `adarsh165787/frontend` tag `latest`)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                  [INSERT SCREENSHOT: DOCKER HUB FRONTEND REPO]                  |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

#### Screenshot 5: Docker Hub Backend Repository
*(Capture Docker Hub web page showing `adarsh165787/backend` tag `latest`)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                  [INSERT SCREENSHOT: DOCKER HUB BACKEND REPO]                   |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

---

### 8. CI/CD Execution Details and Evidence

#### 8.1 GitHub Actions Workflow Overview
- `.github/workflows/ci.yml`: Evaluates PR commits via Hadolint, Compose setup, 12 Jest test cases, and database volume persistence test.
- `.github/workflows/cd.yml`: Authenticates with Docker Hub secrets, builds and pushes images, deploys with `docker-compose.deploy.yml`, and verifies health.

#### Screenshot 6: GitHub Actions Workflow Execution
*(Capture GitHub Actions tab showing green checkmarks for all stages)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                   [INSERT SCREENSHOT: GITHUB ACTIONS EXECUTION]                 |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

#### Screenshot 7: Successful Deployment Verification in CD
*(Capture the deployment verification step in CD workflow log)*
```
+---------------------------------------------------------------------------------+
|                                                                                 |
|                 [INSERT SCREENSHOT: CD DEPLOYMENT VERIFICATION]                 |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

---

### 9. Application Deployment Details
- **Deployment Command:** `docker compose -f docker-compose.deploy.yml up -d`
- **Application URL:** `http://localhost:8080/`
- **Backend Health URL:** `http://localhost:3000/health`
- **Database Engine:** PostgreSQL 16
- **Caching Engine:** Redis 7.4

---

### 10. Declaration

"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."

**Student Name:** Adarsh Kumar  
**Roll Number:** 202401100300012  
**Section:** CSE AI-A  
**Date:** 18 November 2026  
**Signature:** __________________________
