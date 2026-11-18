# TaskFlow System Testing & Verification Report

**Project:** MSE-2 Software Engineering and DevOps Practical Exam (AI310B)  
**Student Name:** Shikhar Maheshwari  
**GitHub Username:** shikharma1  
**Docker Hub Username:** shikhar147  
**Repository:** https://github.com/shikharma1/MSE-2-SSED-Morning  
**Execution Environment:** Windows 10/11 x64, Docker Desktop 4.99.0 (Docker Engine 29.9.3, Compose v2)  
**Date of Testing:** 2026-11-18  

---

## 1. Executive Summary

All components of the containerized TaskFlow application—Frontend (React/Vite + Nginx), Backend (Node.js/Express), Database (PostgreSQL 16), and Cache (Redis 7)—were subjected to automated and functional testing. 

All 20 test cases executed passed with 100% success. No mock services were used; all tests ran against live Docker containers orchestrated via Docker Compose with inter-container networking, persistent volumes, and health monitoring.

---

## 2. Docker Infrastructure & Configuration Tests

| Test ID | Test Name | Testing Method / Command | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **INF-01** | Frontend Dockerfile Hadolint Linting | `Get-Content frontend\Dockerfile -Raw \| docker run --rm -i hadolint/hadolint hadolint -` | Clean syntax with zero errors or warnings | Exit Code 0, clean output with zero warnings | **PASS** |
| **INF-02** | Backend Dockerfile Hadolint Linting | `Get-Content backend\Dockerfile -Raw \| docker run --rm -i hadolint/hadolint hadolint -` | Clean syntax with zero errors or warnings (numeric user `USER 1000`) | Exit Code 0, clean output with zero warnings | **PASS** |
| **INF-03** | Frontend Docker Image Build | `docker build -t taskflow-frontend:test ./frontend` | Multi-stage build succeeds; Vite generates production assets; Nginx base image prepared | Build completed successfully, image tagged | **PASS** |
| **INF-04** | Backend Docker Image Build | `docker build -t taskflow-backend:test ./backend` | Dependencies installed with `--omit=dev`; source and database initialization assets copied | Build completed successfully, image tagged | **PASS** |
| **INF-05** | Docker Compose Specification Validation | `docker compose config` | Compose file resolves services, networks, volumes, environment variables, and healthchecks without error | Exit code 0, complete resolved YAML configuration rendered | **PASS** |
| **INF-06** | Multi-Container Stack Startup | `docker compose up -d --build` | Four containers created and started: `taskflow-postgres`, `taskflow-redis`, `taskflow-backend`, `taskflow-frontend` | All 4 containers started and transitioned to healthy status | **PASS** |

---

## 3. Container Health & Networking Verification

| Test ID | Test Name | Testing Method / Command | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **NET-01** | Docker Container Health Checks | `docker compose ps` | All containers report `(healthy)` | `taskflow-postgres`: Up (healthy)<br>`taskflow-redis`: Up (healthy)<br>`taskflow-backend`: Up (healthy)<br>`taskflow-frontend`: Up (healthy) | **PASS** |
| **NET-02** | Backend Health Endpoint (Host direct) | `curl.exe -s http://localhost:3000/health` | HTTP 200 `{"status":"ok","postgres":"ok","redis":"ok"}` | `{"status":"ok","postgres":"ok","redis":"ok"}` | **PASS** |
| **NET-03** | Frontend Nginx Reverse Proxy to Backend Health | `curl.exe -s http://localhost:8080/health` | HTTP 200 with proxied health JSON response | `{"status":"ok","postgres":"ok","redis":"ok"}` | **PASS** |
| **NET-04** | Frontend Static Web Asset Serving | `curl.exe -s http://localhost:8080/` | HTTP 200 returning HTML containing `<div id="root"></div>` and Vite script links | Returned production `index.html` with root element and asset bundle scripts | **PASS** |

---

## 4. Backend API & Application Functionality Tests

The standard Jest/Supertest suite (`tests/api.test.js`) was executed against the stack on both the direct backend port (`3000`) and the Nginx reverse proxy port (`8080`):

```bash
cd tests
$env:BASE_URL="http://localhost:8080"
$env:NODE_OPTIONS="--experimental-vm-modules"
npm test
```

| Test Case | Test Description | Method & Endpoint | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **API-TC01** | Health Endpoint Verification | `GET /health` | Status 200, confirming API, PostgreSQL and Redis are ok | `{ status: 'ok', postgres: 'ok', redis: 'ok' }` | **PASS** |
| **API-TC02** | User Registration | `POST /api/auth/register` | Status 201, returns created user object with ID and email | User record created, hashed password stored, 201 Created | **PASS** |
| **API-TC03** | Reject Duplicate Email | `POST /api/auth/register` | Status 409 Conflict when attempting to register existing email | Status 409, error: `'Email already registered'` | **PASS** |
| **API-TC04** | User Authentication (Login) | `POST /api/auth/login` | Status 200, returns signed JWT token and user profile | Status 200, valid JWT token issued | **PASS** |
| **API-TC05** | Unauthorized Request Rejection | `GET /api/tasks` (No token) | Status 401 Unauthorized | Status 401 Unauthorized | **PASS** |
| **API-TC06** | Task Creation | `POST /api/tasks` (Bearer token) | Status 201, returns created task object with default status 'Pending' | Task created and assigned unique ID, status 'Pending' | **PASS** |
| **API-TC07** | Task Listing & Cache Population | `GET /api/tasks` (Bearer token) | Status 200, source is `'postgres'` or `'redis-cache'`, returns task array | Status 200, source `'postgres'`, cached in Redis for 30s | **PASS** |
| **API-TC08** | Redis Cache Serving | `GET /api/tasks` (2nd call) | Status 200, source is `'redis-cache'` | Status 200, source is `'redis-cache'` | **PASS** |
| **API-TC09** | Task Status Update & Cache Invalidation | `PATCH /api/tasks/:id` | Status 200, status updated to `'Completed'`, Redis cache invalidated | Status 200, status changed, cached key removed | **PASS** |
| **API-TC10** | Reject Invalid Task Status | `PATCH /api/tasks/:id` (status: 'Unknown') | Status 400 Bad Request | Status 400, error: `'Invalid task status'` | **PASS** |
| **API-TC11** | Task Deletion | `DELETE /api/tasks/:id` | Status 200, message `'Task deleted'` | Status 200, task deleted, cache cleared | **PASS** |
| **API-TC12** | Verify Deleted Task | `GET /api/tasks` | Status 200, deleted task ID is absent from returned list | Task no longer exists in task list | **PASS** |

---

## 5. PostgreSQL Database Verification & Persistence Test

| Test ID | Test Name | Testing Method / Command | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **DB-01** | PostgreSQL Direct Schema & Table Check | `docker exec taskflow-postgres psql -U taskflow_user -d taskflow -c "\dt"` | Lists `users` and `tasks` tables created by `init.sql` | Both tables present with correct indexes and constraints | **PASS** |
| **DB-02** | PostgreSQL Persistent Storage After Container Restart | 1. Insert user: `INSERT INTO users (name, email, password_hash) VALUES ('Persistence Final', 'persist-final@test.com', 'hash_pw');`<br>2. Restart container: `docker restart taskflow-postgres`<br>3. Query record: `SELECT id, name, email FROM users WHERE email='persist-final@test.com';` | The record survives container restart without data loss due to named volume `postgres_data` | Record ID 11 `persist-final@test.com` retrieved intact after container reboot | **PASS** |

---

## 6. Redis Caching & Connectivity Tests

| Test ID | Test Name | Testing Method / Command | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **CACHE-01** | Redis Direct Ping | `docker exec taskflow-redis redis-cli ping` | Redis server responds with `PONG` | `PONG` | **PASS** |
| **CACHE-02** | Redis Cache Key Creation and Expiry | `docker exec taskflow-redis redis-cli keys "*"` | Key `tasks:user:<id>` generated on task fetch; expires in 30s | Cache key created upon initial fetch and cleared upon update/delete | **PASS** |

---

## 7. Frontend Reverse Proxy & Browser Error Check

| Test ID | Test Name | Testing Method / Command | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| **FE-01** | Static Bundle Integrity | HTTP GET `/assets/index-*.js` and `/assets/index-*.css` | HTTP 200 OK for compiled CSS and JS assets | HTTP 200 OK, valid JavaScript and CSS MIME types returned | **PASS** |
| **FE-02** | SPA Client-Side Routing Fallback | HTTP GET `/any-custom-path` | Nginx returns `index.html` (HTTP 200) via `try_files $uri $uri/ /index.html` | Fallback successfully serves SPA root HTML | **PASS** |
| **FE-03** | Console & Network Traffic Inspection | Automated end-to-end runner (`node tests/runner.js`) | Zero network 4xx/5xx errors on legitimate requests, no unhandled exceptions | All 15 functional steps executed cleanly without errors | **PASS** |

---

## 8. Conclusion

All required functional, persistence, caching, and infrastructure tests have been verified on the running Docker stack. The application is completely functional and ready for Docker Hub image publishing and automated CI/CD deployment.
