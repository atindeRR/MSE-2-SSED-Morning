# MSE-2 Software Engineering & DevOps Practical Examination Documentation
**Document Name:** `2400291520290_Yuvraj_Singh.pdf`

---

## 1. Student Information

- **Full Name:** Yuvraj Singh
- **University Roll Number:** 2400291520290
- **Section:** D
- **Branch:** CSE (AI)
- **GitHub Username:** ItsmeYuvi

---

## 2. GitHub Submission Details

- **GitHub Repository URL (Personal Fork):** https://github.com/ItsmeYuvi/MSE-2-SSED-Morning
- **GitHub Branch Used for Implementation:** `main`
- **Upstream Starter Repository:** https://github.com/atindeRR/MSE-2-SSED-Morning

---

## 3. Docker Hub Details

- **Docker Hub Username:** yuviiii2309
- **Frontend Docker Image URL:** https://hub.docker.com/r/yuviiii2309/frontend
- **Backend Docker Image URL:** https://hub.docker.com/r/yuviiii2309/backend

---

## 4. Container Architecture & Implementation Summary

- **Frontend (`frontend/Dockerfile`):** Multi-stage Docker build utilizing `node:20-alpine` for building React/Vite assets and `nginx:1.27-alpine` for production serving on port 80 (mapped to 8080). Configured reverse proxy for `/api/` and `/health` to `http://backend:3000`.
- **Backend (`backend/Dockerfile`):** Production Node.js 20 container running as non-root user (`USER 1000`) with optimized `npm ci --omit=dev` layer caching, listening on port 3000.
- **Database (`postgres:16-alpine`):** PostgreSQL database with named volume persistence (`postgres_data`) and automatic initialization (`init.sql`).
- **Cache (`redis:7-alpine`):** In-memory cache for API task endpoints with health-checked readiness.
- **Docker Compose:** Complete orchestration defined in `docker-compose.yml` (build-enabled) and `docker-compose.deploy.yml` (pure image pull).

---

## 5. CI/CD Execution Evidence & Verification

### 5.1 Pipeline Execution Stages
1. **Repository Checkout:** `actions/checkout@v4` checks out the code repository.
2. **Buildx Setup:** `docker/setup-buildx-action@v3` configures Docker Buildx.
3. **Docker Hub Authentication:** `docker/login-action@v3` authenticates with `DOCKERHUB_USERNAME` (`yuviiii2309`) and `DOCKERHUB_TOKEN`.
4. **Backend Build & Publishing:** Builds and pushes `yuviiii2309/backend:latest` and `yuviiii2309/backend:<sha>` (as well as `taskflow-backend`).
5. **Frontend Build & Publishing:** Builds and pushes `yuviiii2309/frontend:latest` and `yuviiii2309/frontend:<sha>` (as well as `taskflow-frontend`).
6. **Deployment Compose Pull:** `docker compose -f docker-compose.deploy.yml pull` pulls published images.
7. **Application Deployment:** `docker compose -f docker-compose.deploy.yml up -d` starts the four services on an isolated bridge network.
8. **Health & Endpoint Verification:** Polling confirms backend is healthy on `http://localhost:3000/health` and frontend responds on `http://localhost:8080/`.
9. **Automated API & Integration Tests:** Executes Jest test suite against the live deployment, passing all 12 test cases.

---

## 6. Local & Deployment Test Verification Results

- **Hadolint Linting:** 0 errors, 0 warnings on both `frontend/Dockerfile` and `backend/Dockerfile`.
- **Docker Compose Config:** Both `docker-compose.yml` and `docker-compose.deploy.yml` pass syntax and configuration validation with zero errors.
- **Image Deployment:** All 4 containers (`frontend`, `backend`, `postgres`, `redis`) reach `healthy` status.
- **Direct Health Check:** `http://localhost:3000/health` -> `{"status":"ok","postgres":"ok","redis":"ok"}`.
- **Nginx Reverse Proxy Health Check:** `http://localhost:8080/health` -> `{"status":"ok","postgres":"ok","redis":"ok"}`.
- **Frontend Accessibility:** `http://localhost:8080/` -> HTTP 200 OK.
- **PostgreSQL Persistence:** Data confirmed persistent across container restarts via named volume `postgres_data`.
- **Redis Caching:** Confirmed caching responses and cache invalidation upon task mutations.
- **Jest Test Suite:** 12 of 12 test cases passed (`TC01` through `TC12`).

---

## 7. Declaration

"I hereby declare that the submitted Docker implementation is my own work. I have successfully executed and verified the required CI/CD pipeline stages, published the Docker images to my Docker Hub account, and tested the application deployment."

---
**Student Name:** Yuvraj Singh  
**Roll Number:** 2400291520290  
**Section:** D  
**Branch:** CSE (AI)  
**Date:** November 18, 2026
