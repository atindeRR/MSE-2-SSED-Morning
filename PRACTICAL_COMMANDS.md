# Practical Exam Command Reference Sheet — MSE-2 (AI310B)

Quick reference of all essential Git, Docker, Docker Compose, Docker Hub, and verification commands used in the TaskFlow practical examination.

---

## 1. Git Setup, Cloning & Pushing

```bash
# Clone your personal fork
git clone https://github.com/<YOUR_GITHUB_USERNAME>/MSE-2-SSED-Morning.git
cd MSE-2-SSED-Morning

# Check remotes (origin = your fork, upstream = instructor starter repo)
git remote -v

# Add instructor repository as upstream (if needed)
git remote add upstream https://github.com/atindeRR/MSE-2-SSED-Morning.git

# Check working tree status and branch
git status
git branch -a

# Stage, commit, and push changes to main (triggers CD pipeline)
git add .
git commit -m "Implement Docker containerization and deployment"
git push origin main

# View recent commits
git log -n 5 --oneline
```

---

## 2. Environment Setup

```bash
# Create local .env from template (NEVER commit .env!)
cp .env.example .env
# Edit .env and set secure POSTGRES_PASSWORD, DATABASE_URL, JWT_SECRET, DOCKERHUB_USERNAME
```

---

## 3. Dockerfile Linting (Hadolint — Same Check as CI)

```bash
# Lint frontend Dockerfile
docker run --rm -i hadolint/hadolint < frontend/Dockerfile

# Lint backend Dockerfile
docker run --rm -i hadolint/hadolint < backend/Dockerfile
```

---

## 4. Building Docker Images

```bash
# Build frontend and backend images individually
docker build -t <YOUR_DOCKERHUB_USERNAME>/taskflow-frontend:latest ./frontend
docker build -t <YOUR_DOCKERHUB_USERNAME>/taskflow-backend:latest ./backend

# Also tag with README repository names if desired
docker tag <YOUR_DOCKERHUB_USERNAME>/taskflow-frontend:latest <YOUR_DOCKERHUB_USERNAME>/frontend:latest
docker tag <YOUR_DOCKERHUB_USERNAME>/taskflow-backend:latest <YOUR_DOCKERHUB_USERNAME>/backend:latest

# Or build via Docker Compose
docker compose build
```

---

## 5. Docker Compose Validation, Startup & Shutdown (Local Build)

```bash
# Validate docker-compose.yml syntax and variable interpolation
docker compose config
docker compose config --quiet

# Build and start all 4 services in detached mode
docker compose up -d --build

# Start without rebuilding
docker compose up -d

# Stop containers (preserves containers and volumes)
docker compose stop

# Stop and remove containers & networks (PRESERVES PostgreSQL volume!)
docker compose down

# Stop and remove containers, networks AND volumes (WIPES database!)
docker compose down -v
```

---

## 6. Inspecting Images, Containers, Networks, Volumes & Logs

```bash
# Check Compose service status & health
docker compose ps

# Check all containers and Container IDs
docker ps -a

# Check local images, tags, and Image IDs
docker images

# Inspect image digests
docker images --digests

# View logs for all services
docker compose logs

# Follow live logs for a specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres
docker compose logs -f redis

# Inspect networks and volumes
docker network ls
docker volume ls
```

---

## 7. Testing Application Endpoints, Redis Cache & PostgreSQL Persistence

```bash
# Check backend health (verifies Express + PostgreSQL + Redis)
curl http://localhost:3000/health

# Check frontend availability (via Nginx)
curl -I http://localhost:8080/

# Check Nginx reverse proxy to backend health
curl http://localhost:8080/health

# Run the automated 12-test Jest + Supertest API & Redis suite
cd tests
npm install
BASE_URL=http://localhost:3000 NODE_OPTIONS=--experimental-vm-modules npm test
cd ..

# Verify PostgreSQL persistence (recreate containers WITHOUT -v)
docker compose down
docker compose up -d
# Verify previously created users/tasks still exist in PostgreSQL:
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, name, email FROM users;"
docker compose exec postgres psql -U taskflow_user -d taskflow -c "SELECT id, title, status FROM tasks;"

# Verify Redis connectivity
docker compose exec redis redis-cli PING
```

---

## 8. Docker Hub Login, Tagging & Pushing

```bash
# Authenticate with Docker Hub (use username + Personal Access Token)
docker login

# Push images matching cd.yml & docker-compose.deploy.yml
docker push <YOUR_DOCKERHUB_USERNAME>/taskflow-frontend:latest
docker push <YOUR_DOCKERHUB_USERNAME>/taskflow-backend:latest

# Push images matching README naming convention
docker push <YOUR_DOCKERHUB_USERNAME>/frontend:latest
docker push <YOUR_DOCKERHUB_USERNAME>/backend:latest

# Verify published image manifest/digest remotely
docker buildx imagetools inspect <YOUR_DOCKERHUB_USERNAME>/taskflow-frontend:latest
docker buildx imagetools inspect <YOUR_DOCKERHUB_USERNAME>/taskflow-backend:latest
```

---

## 9. Deployment Using Published Docker Hub Images (`docker-compose.deploy.yml`)

```bash
# Validate deployment compose file
docker compose -f docker-compose.deploy.yml config --quiet

# Pull pre-built images from Docker Hub (NO local build!)
docker compose -f docker-compose.deploy.yml pull

# Start the application using published images
docker compose -f docker-compose.deploy.yml up -d

# Check container status and logs
docker compose -f docker-compose.deploy.yml ps
docker compose -f docker-compose.deploy.yml logs

# Verify health and frontend
curl http://localhost:3000/health
curl -I http://localhost:8080/

# Tear down deployment stack
docker compose -f docker-compose.deploy.yml down
```

---

## 10. GitHub Actions CI/CD Verification Checklist

1. Configure GitHub Secrets in **Your Fork → Settings → Secrets and variables → Actions**:
   - `DOCKERHUB_USERNAME`
   - `DOCKERHUB_TOKEN`
   - `POSTGRES_PASSWORD`
2. Push to `main`: `git push origin main`
3. Open **Your Fork → Actions → Docker Practical - Publish and Verify**
4. Confirm every stage is green:
   - Checkout → Validate secrets → Buildx → Docker Hub Login → Build & push backend → Build & push frontend → Create `.env` → Validate `docker-compose.deploy.yml` → Pull images → Deploy → Verify `/health` & `/` → Run API tests → Cleanup.
