# Final Submission Report — MSE-2 Practical Examination (AI310B)

**Subject:** Software Engineering and DevOps (AI310B) — Morning Shift  
**Student Name:** Taranjeet Singh Bagga  
**University Roll Number:** `202401100300263`  
**Section / Branch:** `D` / `CSE-AI`  
**GitHub Username:** `Taran790`  
**Docker Hub Username:** `tarrrrannnnnn`

---

## 1. Requirements Completion Checklist

- [x] Repository inspected & application architecture analyzed (`PROJECT_ANALYSIS.md`)
- [x] Frontend multi-stage Dockerfile created (`frontend/Dockerfile`, Hadolint exit code `0`)
- [x] Backend production Dockerfile created (`backend/Dockerfile`, Hadolint exit code `0`)
- [x] Frontend & Backend `.dockerignore` files hardened
- [x] `docker-compose.yml` implemented (4 services, custom bridge network, named volume, health checks)
- [x] Environment variables & security configured (`.env.example`, `.gitignore`, no hardcoded secrets)
- [x] PostgreSQL persistent volume (`postgres_data`) & `init.sql` initialization verified across container recreation
- [x] Redis caching (`postgres` -> `redis-cache` + invalidation on writes) verified
- [x] All 4 local containers built, started, healthy, and verified (`12/12` Jest tests passed)
- [x] Frontend & Backend Docker images published to Docker Hub (`tarrrrannnnnn`) and verified public
- [x] `docker-compose.deploy.yml` created (published Docker Hub images only, zero `build:` directives)
- [x] Published images pulled and deployed locally (`12/12` Jest tests passed)
- [x] GitHub Actions secrets configured and CD pipeline (`cd.yml`) executed & **PASSED (Success, 1m 16s)**
- [x] Personal fork (`Taran790/MSE-2-SSED`, `main`) updated and verified
- [x] Real screenshots & logs saved in `deployment-evidence/`
- [x] Final submission documents generated in exact 5-section question-paper format (`202401100300263_Taranjeet_Singh_Bagga.pdf` & `202401100300263_Taranjeet_Singh_Bagga.docx`)
- [x] Viva preparation (`VIVA_QUESTIONS.md`) & Practical Command Sheet (`PRACTICAL_COMMANDS.md`) created
- [x] Final Pull Request created: https://github.com/atindeRR/MSE-2-SSED-Morning/pull/46 (`DOCKER-EXAM | 202401100300263 | Taranjeet Singh Bagga | D`)

---

## 2. Files Created or Modified

| File | Action | Purpose |
|---|---|---|
| `frontend/Dockerfile` | Modified | Multi-stage `node:20-alpine` -> `nginx:1.27-alpine` build with `HEALTHCHECK` |
| `frontend/.dockerignore` | Modified | Excludes `node_modules`, `dist`, `.env*`, `.git`, `Dockerfile`, docs |
| `backend/Dockerfile` | Modified | Production `node:20-alpine`, non-root `USER 1000:1000`, Node 20 `HEALTHCHECK` |
| `backend/.dockerignore` | Modified | Excludes `node_modules`, `.env*`, `tests`, `db`, `.git`, docs |
| `docker-compose.yml` | Created | Local build orchestration for `postgres`, `redis`, `backend`, `frontend` |
| `docker-compose.deploy.yml` | Created | Zero-build deployment using published Docker Hub images |
| `.env.example` | Modified | Documented environment variable placeholders (incl. `DOCKERHUB_USERNAME`) |
| `.gitignore` | Modified | Protects `.env`, `.env.*` (while keeping `.env.example`) |
| `submission.json` | Created | Structured student & image metadata checked by `ci.yml` |
| `PROJECT_ANALYSIS.md` | Created | Complete Phase 1 repository and architecture analysis |
| `VIVA_QUESTIONS.md` | Created | 58 oral examination questions and concise answers |
| `PRACTICAL_COMMANDS.md` | Created | Practical exam command reference sheet |
| `202401100300263_Taranjeet_Singh_Bagga.doc` | Created | Self-contained Microsoft Word submission document with embedded screenshots |
| `202401100300263_Taranjeet_Singh_Bagga.pdf` | Created | Mandatory PDF submission document with embedded screenshots |
| `FINAL_SUBMISSION_REPORT.md` | Created | This final verification & handoff report |
| `deployment-evidence/` | Created | Saved local, deploy, Docker Hub, and GitHub Actions logs & screenshots |

---

## 3. Docker Images & Published Docker Hub URLs

### Local Built Images
| Image | Tag | Image ID | Size |
|---|---|---|---|
| `taskflow-frontend` | `local` | `83dc40fe81f9` | `73.8 MB` |
| `taskflow-backend` | `local` | `ab6e81367ed1` | `206 MB` |
| `postgres` | `16-alpine` | `81e77a483348` | `420 MB` |
| `redis` | `7-alpine` | `7f7d30b7fdd0` | `58.5 MB` |

### Published Docker Hub Images (Verified Public & Live)
| Repository | Tag | Docker Hub URL | Verified Manifest Digest (CD Buildx `linux/amd64`) |
|---|---|---|---|
| `tarrrrannnnnn/taskflow-frontend` | `latest` | https://hub.docker.com/r/tarrrrannnnnn/taskflow-frontend | `sha256:4c44f5f5227dc71a4bf9c9fac3634b01cccf9fd4a37791c20446cfe7e5b82350` |
| `tarrrrannnnnn/taskflow-backend` | `latest` | https://hub.docker.com/r/tarrrrannnnnn/taskflow-backend | `sha256:f126e65b32642d76d154f3f40e75b82f1211ebff36075aa697ff2edb4fa86204` |
| `tarrrrannnnnn/frontend` | `latest` | https://hub.docker.com/r/tarrrrannnnnn/frontend | `sha256:54a494ea36f6a0de603a2a4c8d2a98f85faed1a53542e8178199b43727b303dd` |
| `tarrrrannnnnn/backend` | `latest` | https://hub.docker.com/r/tarrrrannnnnn/backend | `sha256:1595926a22ee2446f233b022f954f63e5ff69f4ea28c21456297a490a59506f2` |

---

## 4. Verified Container Names & IDs

### Local Build Deployment (`docker-compose.yml`)
- `mse-2-frontend-1` (`551646fc9015`) — `taskflow-frontend:local` — `Up (healthy)` — `0.0.0.0:8080->80/tcp`
- `mse-2-backend-1` (`54cabbe24f4e`) — `taskflow-backend:local` — `Up (healthy)` — `0.0.0.0:3000->3000/tcp`
- `mse-2-postgres-1` (`51edacdec6e7`) — `postgres:16-alpine` — `Up (healthy)` — `5432/tcp` (internal)
- `mse-2-redis-1` (`6fdfec4db3fa`) — `redis:7-alpine` — `Up (healthy)` — `6379/tcp` (internal)

### Published Image Deployment (`docker-compose.deploy.yml`)
- `mse-2-frontend-1` (`e1bd2a3c12fd`) — `tarrrrannnnnn/taskflow-frontend:latest` — `Up (healthy)` — `0.0.0.0:8080->80/tcp`
- `mse-2-backend-1` (`fb4a034119fb`) — `tarrrrannnnnn/taskflow-backend:latest` — `Up (healthy)` — `0.0.0.0:3000->3000/tcp`
- `mse-2-postgres-1` (`0e680cc51e38`) — `postgres:16-alpine` — `Up (healthy)` — `5432/tcp` (internal)
- `mse-2-redis-1` (`de03f91f1496`) — `redis:7-alpine` — `Up (healthy)` — `6379/tcp` (internal)

---

## 5. Testing Summary

| Test Category | Result | Evidence File |
|---|---|---|
| **Hadolint (`frontend/Dockerfile` & `backend/Dockerfile`)** | **PASS** (Exit code `0`, 0 warnings) | Verified locally via `hadolint/hadolint` |
| **Local Stack Health & Nginx Reverse Proxy** | **PASS** (`{"status":"ok","postgres":"ok","redis":"ok"}` on `:3000/health` & `:8080/health`, HTTP `200` on `:8080/`) | `deployment-evidence/local/backend-health.json` |
| **Local Jest API & Redis Suite (`tests/api.test.js`)** | **12/12 PASSED** | `deployment-evidence/local/jest-api-tests.txt` |
| **PostgreSQL Persistence Across Container Recreation** | **PASS** (Task ID 2 `"Persistence Check Task"` survived `docker compose down && docker compose up -d`) | `deployment-evidence/local/persistence-test.txt` |
| **Redis Cache Hit & Invalidation** | **PASS** (`1st GET: postgres`, `2nd GET: redis-cache`, invalidated on `PATCH`/`DELETE`) | `deployment-evidence/local/jest-api-tests.txt` |
| **Docker Hub Image Deployment (`docker-compose.deploy.yml`)** | **PASS** (`pull` + `up -d` + **12/12 Jest tests PASSED**) | `deployment-evidence/deploy/jest-deploy-tests.txt` |

---

## 6. GitHub Actions CI/CD Verification

- **Workflow Name:** `Docker Practical - Publish and Verify` (`.github/workflows/cd.yml`)
- **Latest CD Workflow Run URL (Push-triggered #2):** https://github.com/Taran790/MSE-2-SSED/actions/runs/44245697870 (`main`, commit `8854f70`, **Success**, `1m 7s`)
- **Initial CD Workflow Run URL (Manual #1):** https://github.com/Taran790/MSE-2-SSED/actions/runs/44244755677 (`main`, commit `411e99b`, **Success**, `1m 16s`)
- **Final Status:** **Success** (all 15 steps green on both runs)

---

## 7. Submission Documents & Evidence Directory

- **Mandatory PDF Document (`.pdf`):** `202401100300263_Taranjeet_Singh_Bagga.pdf` (exact 5-section question-paper format)
- **Editable Word Document (`.docx`):** `202401100300263_Taranjeet_Singh_Bagga.docx` (exact 5-section question-paper format)
- **Evidence Directory:**
  - `deployment-evidence/local/` — container lists, images, logs, Jest output, persistence test, TaskFlow UI & `/health` screenshots
  - `deployment-evidence/dockerhub/` — verified public tag digests
  - `deployment-evidence/deploy/` — `docker-compose.deploy.yml` pull, containers, health, logs, Jest output
  - `deployment-evidence/github-actions/` — `github-fork-repo.png`, `cd-workflow-list.png`, `cd-run2-summary.png`, `cd-run2-job.png`, `pr-46.png`, `pr-46-checks.png`

---

## 8. Pull Request Submission Details (Submitted & Open)

- **Final Pull Request URL:** https://github.com/atindeRR/MSE-2-SSED-Morning/pull/46
- **Base Repository:** `atindeRR/MSE-2-SSED-Morning` (`main`)
- **Head Repository:** `Taran790/MSE-2-SSED` (`main`)
- **Pull Request Title:**
  ```text
  DOCKER-EXAM | 202401100300263 | Taranjeet Singh Bagga | D
  ```

---

## 9. Cleanup Instructions (After Viva / Grading)

```bash
# Stop and remove containers while preserving PostgreSQL data:
docker compose -f docker-compose.deploy.yml down

# Stop and remove containers AND delete PostgreSQL volume (complete reset):
docker compose -f docker-compose.deploy.yml down -v
```
