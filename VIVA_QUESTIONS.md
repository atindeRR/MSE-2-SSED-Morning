# Viva & Practical Examination Preparation — MSE-2 (AI310B)

**Subject:** Software Engineering and DevOps (AI310B)  
**Project:** TaskFlow (React + Vite + Nginx, Node.js + Express, PostgreSQL, Redis)

---

## Section 1: Docker Fundamentals

### Q1. What is Docker?
**Answer:** Docker is an open-source platform that packages an application together with all its dependencies, libraries, and configuration into a lightweight, portable unit called a **container**. This guarantees the application runs the same way on a student's laptop, a teammate's machine, and a CI/CD runner.

### Q2. What is containerization?
**Answer:** Containerization is OS-level virtualization where applications run in isolated user-space environments sharing the host OS kernel. Unlike Virtual Machines (VMs), containers do not need a separate guest operating system, making them much faster to start and far lighter on RAM and disk space.

### Q3. What is a Docker image?
**Answer:** A Docker image is a **read-only blueprint/template** containing everything needed to run an application: base OS files, runtime (Node.js or Nginx), dependencies, compiled code, and startup instructions. Images are built from a `Dockerfile`.

### Q4. What is a Docker container?
**Answer:** A Docker container is a **running (or stopped) instance** of a Docker image. It adds a thin writable layer on top of the read-only image layers and runs an isolated process with its own filesystem, network interface, and environment variables.

### Q5. What is the difference between a Docker image and a Docker container?
**Answer:** An **image** is static and read-only (like a class in OOP or a recipe). A **container** is a live, executable runtime instance created from an image (like an object or a cooked dish). You can create multiple independent containers from the same image.

### Q6. What is a Dockerfile?
**Answer:** A `Dockerfile` is a plain-text build script containing step-by-step instructions (`FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`, `HEALTHCHECK`) that Docker executes sequentially to assemble a Docker image.

### Q7. What is a Docker layer and how does build caching work?
**Answer:** Each instruction in a `Dockerfile` (`FROM`, `COPY`, `RUN`) creates an immutable filesystem **layer**. Docker caches layers: if a layer and its inputs have not changed, Docker reuses the cached layer instead of rebuilding it. That is why we copy `package*.json` and run `npm install` *before* copying `src/`—so code edits don't force reinstalling dependencies every time.

### Q8. What is a multi-stage build, and why did we use it for the frontend?
**Answer:** A multi-stage build uses multiple `FROM` instructions in one `Dockerfile`. In `frontend/Dockerfile`:
- **Stage 1 (`node:20-alpine AS builder`)** installs npm packages and runs `vite build` to compile React JSX/CSS into static files in `/app/dist`.
- **Stage 2 (`nginx:1.27-alpine`)** copies *only* `/app/dist` and `nginx.conf`, discarding Node.js, Vite, and `node_modules`.
This shrinks the final frontend image drastically and reduces its security attack surface.

### Q9. What is a Docker volume?
**Answer:** A Docker volume is Docker-managed persistent storage stored on the host outside a container's writable layer. Even if a container is stopped, deleted, or recreated, data stored in a named volume (like `postgres_data`) survives intact.

### Q10. What is a Docker network?
**Answer:** A Docker network connects containers together so they can communicate securely. On a user-defined bridge network (`taskflow-net`), Docker provides built-in **automatic DNS resolution**, allowing containers to reach each other by their Compose service names (`postgres`, `redis`, `backend`).

### Q11. What is port mapping (`-p` / `ports`)?
**Answer:** Port mapping binds a port on the host machine to a port inside a container using the format `HOST_PORT:CONTAINER_PORT`. For example, `"8080:80"` maps port `8080` on localhost to Nginx's port `80` inside the frontend container, while `"3000:3000"` exposes the Express API.

### Q12. What is a container registry?
**Answer:** A container registry (such as Docker Hub, GitHub Container Registry, or AWS ECR) is a centralized server for storing, versioning, and distributing Docker images so any machine or CI/CD runner can pull and deploy them.

### Q13. What is `.dockerignore` and why is it important?
**Answer:** `.dockerignore` lists files and folders (like `node_modules`, `.env`, `.git`, `dist`) that Docker excludes from the build context sent to the Docker daemon. This speeds up builds, keeps images small, and prevents accidentally baking secrets (`.env`) into an image.

### Q14. Why do we run the backend container as a non-root user (`USER node`)?
**Answer:** Running a container as `root` is a security risk: if an attacker compromises the Express app, they gain root privileges inside the container. Using the built-in unprivileged `node` user follows the **principle of least privilege**.

### Q15. What is the difference between `CMD` and `ENTRYPOINT`?
**Answer:** `CMD` sets the default command/arguments executed when a container starts and can be easily overridden at runtime (`docker run image sh`). `ENTRYPOINT` configures the fixed main executable of the container so arguments passed at runtime are appended to it.

### Q16. What is the difference between `COPY` and `ADD` in a Dockerfile?
**Answer:** `COPY` transparently copies local files/directories into the image and is preferred for clarity. `ADD` has extra implicit behaviors (auto-extracting local tar archives and fetching remote URLs), so best practice (and Hadolint) recommends `COPY` unless extraction is explicitly needed.

### Q17. Why do we use Alpine-based images (`node:20-alpine`, `nginx:1.27-alpine`, `postgres:16-alpine`, `redis:7-alpine`)?
**Answer:** Alpine Linux is a minimal Linux distribution (~5 MB). Alpine-based official images are much smaller, download and push faster to Docker Hub, and contain fewer packages (smaller attack surface) than full Debian/Ubuntu images.

### Q18. What is Hadolint?
**Answer:** Hadolint is a Dockerfile linter used in our CI workflow (`ci.yml`). It inspects Dockerfiles against industry best practices (e.g., pinned base image versions, proper `WORKDIR`, clean package installation, valid `HEALTHCHECK`) and fails the pipeline if bad practices are detected.

---

## Section 2: Docker Compose

### Q19. What is Docker Compose?
**Answer:** Docker Compose is a tool for defining and running multi-container Docker applications using a declarative YAML file (`docker-compose.yml`). With a single command (`docker compose up -d`), it creates networks, volumes, and all four containers together.

### Q20. Why do we use `docker-compose.yml`?
**Answer:** Without Compose, starting 4 interdependent containers (`postgres`, `redis`, `backend`, `frontend`) would require long, error-prone `docker run` commands with manual network creation, volume flags, and environment variables. `docker-compose.yml` makes the entire stack reproducible and version-controlled.

### Q21. What is a "service" in Docker Compose?
**Answer:** A service is a container definition inside the `services:` section of a Compose file. Our stack has four services: `frontend`, `backend`, `postgres`, and `redis`.

### Q22. What is `depends_on` and why do we pair it with `condition: service_healthy`?
**Answer:** Plain `depends_on` only waits for a container to *start*, not for the software inside (like PostgreSQL) to finish initializing. Pairing `depends_on` with `condition: service_healthy` makes Docker Compose wait until the dependency's `healthcheck` passes before starting dependent services (`backend` waits for `postgres` & `redis`; `frontend` waits for `backend`).

### Q23. What are Docker health checks?
**Answer:** A `healthcheck` is a periodic command Docker runs inside a container to verify the service is actually working (not merely running):
- **PostgreSQL:** `pg_isready`
- **Redis:** `redis-cli ping`
- **Backend:** HTTP request to `http://127.0.0.1:3000/health` (which checks both PostgreSQL and Redis)
- **Frontend:** HTTP check on `http://127.0.0.1/`

### Q24. What is a named volume vs a bind mount?
**Answer:**
- **Named volume** (`postgres_data:/var/lib/postgresql/data`): Managed by Docker; ideal for persistent database storage across container restarts and recreations.
- **Bind mount** (`./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro`): Maps a specific host file/folder into the container; here we mount `init.sql` read-only (`:ro`) so PostgreSQL creates the `users` and `tasks` tables on first boot.

### Q25. How do services communicate inside Docker Compose?
**Answer:** All four services join the custom bridge network `taskflow-net`. Docker's embedded DNS server automatically resolves each service's name (`postgres`, `redis`, `backend`) to that container's private IP address on the bridge network.

### Q26. What is the difference between `build:` and `image:` in Docker Compose?
**Answer:**
- `build:` tells Docker Compose to build an image locally from a `Dockerfile` (used in `docker-compose.yml` for development/CI).
- `image:` tells Docker Compose to pull a pre-built image from a registry like Docker Hub (used in `docker-compose.deploy.yml` for production deployment without local source builds).

### Q27. What is the difference between `docker compose up`, `docker compose stop`, `docker compose down`, and `docker compose down -v`?
**Answer:**
- `docker compose up -d`: Creates and starts containers, networks, and volumes in detached (background) mode.
- `docker compose stop`: Stops running containers without removing them.
- `docker compose down`: Stops and **removes** containers and networks, **preserving** named volumes (`postgres_data` survives!).
- `docker compose down -v`: Stops and removes containers, networks, **AND deletes named volumes** (wipes the PostgreSQL database!).

### Q28. Why did we NOT expose PostgreSQL (`5432`) and Redis (`6379`) ports to the host?
**Answer:** Only the `backend` container needs to talk to PostgreSQL and Redis, and it does so over the private `taskflow-net` Docker network. Leaving `5432` and `6379` unexposed to the host follows security best practices by minimizing external exposure.

### Q29. What does `restart: unless-stopped` do?
**Answer:** It tells Docker to automatically restart a container if it crashes or if the host/Docker daemon reboots, unless the administrator explicitly stopped the container.

---

## Section 3: Application-Specific Architecture (TaskFlow)

### Q30. Why do we use Nginx for the frontend instead of running Vite dev server in production?
**Answer:** Vite's dev server (`vite`) is designed for local hot-reload development—it is slow, unminified, and insecure for production. Nginx is a battle-tested, ultra-fast web server that serves the pre-compiled static bundle (`/usr/share/nginx/html`), handles SPA fallback routing (`try_files`), and acts as a reverse proxy for `/api/` and `/health`.

### Q31. Why does a React application need a production build (`npm run build`)?
**Answer:** Browsers cannot execute JSX or modern modular React code directly. `vite build` transpiles JSX, bundles JavaScript and CSS, tree-shakes unused code, and minifies assets into static HTML/JS/CSS files in `dist/`.

### Q32. What is Vite?
**Answer:** Vite is a modern frontend build tool and development server that uses native ES modules for fast development and Rollup under the hood to generate optimized production bundles (`dist/`).

### Q33. What is Express.js?
**Answer:** Express.js is a minimal web framework for Node.js used to build our REST API (`backend/src/app.js`), handling routing (`/health`, `/api/auth/*`, `/api/tasks/*`), JSON parsing, CORS, JWT authentication middleware, and error handling.

### Q34. Why is PostgreSQL used in TaskFlow?
**Answer:** PostgreSQL is a reliable relational database (RDBMS) that persistently stores structured user accounts (`users` table with unique emails and bcrypt password hashes) and their tasks (`tasks` table with foreign key `user_id` and status check constraints).

### Q35. Why is Redis used in TaskFlow, and how does caching work?
**Answer:** Redis is an in-memory key-value store used for **cache-aside caching** of each user's task list (`tasks:user:<userId>`):
1. On `GET /api/tasks`, the backend first checks Redis. If present, it returns immediately with `"source": "redis-cache"`.
2. On a cache miss, it queries PostgreSQL, caches the result in Redis with a 30-second TTL (`EX: 30`), and returns `"source": "postgres"`.
3. Whenever a user creates, updates, or deletes a task (`POST`/`PATCH`/`DELETE`), the backend calls `redis.del(cacheKey)` to invalidate stale cached data.

### Q36. Why must the backend use service names (`postgres`, `redis`) instead of `localhost`?
**Answer:** Inside a Docker container, `localhost` (127.0.0.1) refers **only to that container itself**, not the host machine or sibling containers. Because PostgreSQL and Redis run in separate containers, connecting to `localhost:5432` from `backend` would fail with `ECONNREFUSED`. Using `postgres:5432` and `redis:6379` resolves to the right containers over Docker's bridge network.

### Q37. How does frontend-to-backend communication work in our containerized setup?
**Answer:** The React app (`frontend/src/main.jsx`) sends API requests to relative URLs starting with `/api` (e.g., `fetch('/api/tasks')`) on the same origin (`http://localhost:8080`). Inside the `frontend` container, `frontend/nginx.conf` intercepts `/api/` and `/health` and reverse-proxies them over Docker's internal network to `http://backend:3000/api/` and `http://backend:3000/health`.

### Q38. How does PostgreSQL automatically create the `users` and `tasks` tables?
**Answer:** The official `postgres` image automatically executes any `.sql` or `.sh` scripts placed in `/docker-entrypoint-initdb.d/` when initializing a brand-new empty data directory. We mount `./backend/db/init.sql` to `/docker-entrypoint-initdb.d/init.sql:ro`.

### Q39. How does the `/health` endpoint work?
**Answer:** In `backend/src/app.js`, `GET /health` executes `SELECT 1` against PostgreSQL and `PING` against Redis. If both succeed, it returns HTTP `200` with `{"status":"ok","postgres":"ok","redis":"ok"}`. If either fails, it returns HTTP `503`.

---

## Section 4: Docker Hub & Image Publishing

### Q40. What is Docker Hub?
**Answer:** Docker Hub (`hub.docker.com`) is the default public container registry operated by Docker where developers host, version, and share Docker images.

### Q41. What is image tagging?
**Answer:** Tagging assigns a registry repository name and version label to an image, formatted as `USERNAME/REPOSITORY:TAG` (e.g., `username/taskflow-backend:latest` or `username/taskflow-backend:<git-sha>`). Tags let you track releases and roll back to specific commits.

### Q42. What is `docker push`?
**Answer:** `docker push` uploads a locally built and tagged image's layers to a remote container registry (like Docker Hub) after authenticating with `docker login`.

### Q43. What is `docker pull`?
**Answer:** `docker pull` downloads a pre-built image from a container registry to the local Docker host so containers can be started without needing source code or rebuilding locally.

### Q44. What is a public repository on Docker Hub?
**Answer:** A public repository allows anyone (including GitHub Actions runners and evaluators) to pull the image without needing private credentials, while only authenticated owners/collaborators can push new versions.

### Q45. Why do we publish images to Docker Hub instead of building on production servers?
**Answer:** Publishing immutable images enables "build once, deploy anywhere": production servers stay clean (no compilers or source code needed), deployments are much faster (just `pull` + `up`), and every environment runs the exact same tested artifact.

### Q46. Why should you use a Docker Hub Access Token instead of your account password in CI/CD?
**Answer:** Personal Access Tokens (PATs) can be scoped to specific permissions (e.g., Read & Write), rotated or revoked independently without changing your main account password, and work cleanly with 2FA-enabled accounts.

---

## Section 5: CI/CD & GitHub Actions

### Q47. What is CI/CD?
**Answer:**
- **CI (Continuous Integration):** Automatically linting, building, and testing code on every pull request or commit (our `ci.yml` runs Hadolint, builds Compose, runs Jest API/Redis tests, and verifies PostgreSQL persistence).
- **CD (Continuous Delivery/Deployment):** Automatically building, publishing Docker images to Docker Hub, pulling them with `docker-compose.deploy.yml`, deploying the stack, and verifying health and API tests on every push to `main` (our `cd.yml`).

### Q48. What is GitHub Actions?
**Answer:** GitHub Actions is GitHub's native CI/CD automation platform that executes workflows defined as YAML files inside `.github/workflows/` on cloud-hosted runners (like `ubuntu-latest`).

### Q49. What is the relationship between a workflow, a job, and a step?
**Answer:**
- **Workflow:** An automated YAML pipeline triggered by events (`push`, `pull_request`, `workflow_dispatch`).
- **Job:** A collection of steps running on the same virtual runner (`publish` in `cd.yml`, `evaluate` in `ci.yml`).
- **Step:** An individual task within a job—either a shell command (`run:`) or a reusable action (`uses: actions/checkout@v4`).

### Q50. What are GitHub Secrets?
**Answer:** GitHub Secrets are encrypted environment variables stored in repository settings (`Settings -> Secrets and variables -> Actions`). They inject sensitive values (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD`) into workflows at runtime and automatically mask them in logs so secrets are never committed to Git.

### Q51. What is Docker Buildx?
**Answer:** Docker Buildx is an extended Docker CLI build plugin powered by **BuildKit**. It provides faster concurrent builds, advanced layer caching, multi-platform image support, and seamless push integration via `docker/build-push-action`.

### Q52. How does our `cd.yml` pipeline publish and verify images?
**Answer:** On push to `main`, `cd.yml`:
1. Checks out code and validates secrets.
2. Sets up Buildx and logs in to Docker Hub.
3. Builds and pushes `taskflow-backend` and `taskflow-frontend` tagged with `:latest` and `:<github.sha>`.
4. Generates `.env` and verifies `docker-compose.deploy.yml` has `image:` and NO `build:`.
5. Pulls the published images, runs `docker compose -f docker-compose.deploy.yml up -d`, verifies `/health` on `:3000` and `/` on `:8080`, and runs all 12 Jest API/Redis tests.

### Q53. How do you troubleshoot a failed GitHub Actions workflow?
**Answer:**
1. Open the failed run in the **Actions** tab and expand the red failed step.
2. Read the exact error message (e.g., missing secret, Hadolint rule violation, wrong image name, container crash, or health check timeout).
3. Inspect container logs printed by `docker compose logs --no-color`.
4. Reproduce the exact failing command locally, fix the root cause, commit, push, and re-verify.

---

## Section 6: Git, GitHub & Submission Workflow

### Q54. What is a GitHub Fork?
**Answer:** A fork is your own personal server-side copy of another user's repository (here, your copy of the instructor's `atindeRR/MSE-2-SSED-Morning`). It gives you full write permissions to push commits, configure Secrets, and run your own CD workflows without modifying the instructor's repo directly.

### Q55. What is a Git Branch?
**Answer:** A branch is an independent movable pointer to a sequence of commits, letting you develop features or fixes in isolation (e.g., `main` or a feature branch) before merging.

### Q56. What is a Pull Request (PR)?
**Answer:** A Pull Request is a formal proposal on GitHub to merge commits from your branch/fork (**head**) into a target repository's branch (**base**). It triggers automated CI checks (`ci.yml`) and allows the instructor to review your code, commit history, and evaluation results.

### Q57. What is the difference between `git commit` and `git push`?
**Answer:** `git commit` saves staged changes to your **local** Git repository history on your laptop. `git push` uploads those local commits to the **remote** GitHub repository (`origin`), which also triggers GitHub Actions workflows.

### Q58. Why is the final Pull Request created against the instructor's repository?
**Answer:** Opening a PR against the instructor's base repository centralizes all student submissions in one place and automatically triggers the instructor's trusted CI evaluation workflow (`ci.yml`) against each student's submitted commit.
