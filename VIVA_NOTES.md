# VIVA NOTES — Docker Practical Exam
> Vivek Kumar | Roll: 2400291520281 | Section: D | CSEAI

---

## 1. Why Multi-Stage Builds?

A **multi-stage build** uses multiple `FROM` statements in one Dockerfile. Each stage produces an intermediate image, and you only copy what you need into the final image.

**Frontend example (our `frontend/Dockerfile`):**
- **Stage 1 (`builder`):** Uses `node:20-alpine`. Installs all dev dependencies, runs `npm run build`, produces the `dist/` folder.
- **Stage 2 (final):** Uses `nginx:alpine`. Copies only `dist/` from Stage 1. No Node.js, no `node_modules`, no dev tools.

**Why it matters:**
- `node:20-alpine` + `node_modules` ≈ 300 MB. `nginx:alpine` + just `dist/` ≈ 25 MB.
- Smaller image = faster pull, less attack surface, lower storage cost.
- Secrets or build-time tokens used in Stage 1 don't leak into the final image.

---

## 2. How the nginx Proxy Works

Our `frontend/nginx.conf`:
```nginx
location /api/ {
    proxy_pass http://backend:3000/api/;  # forwards to backend container
}
location / {
    try_files $uri $uri/ /index.html;     # SPA fallback
}
```

The React app calls `fetch('/api/tasks')` — a **relative URL**. The browser sends this to whatever host serves the page (nginx on port 80 or 8080). Nginx intercepts `/api/` requests and **reverse-proxies** them to `http://backend:3000`. This way:
- No CORS issues (same origin)
- The frontend never needs to know the backend's IP — only the service name `backend`
- The `try_files` line ensures that React Router routes like `/dashboard` serve `index.html` instead of a 404

---

## 3. How the Docker Network Works

In `docker-compose.yml` we define:
```yaml
networks:
  taskflow-net:
    driver: bridge
```
All 4 services join `taskflow-net`. Docker creates an internal DNS server so each container can reach others **by service name**.

- `backend` reaches `postgres:5432` and `redis:6379`
- `nginx` (frontend) reaches `backend:3000`
- Ports are only exposed to the host when you add `ports:` — e.g., `3000:3000` lets your laptop curl the backend

**Why bridge not host?** Bridge isolates the containers from the host network, giving each service its own virtual NIC. The containers talk to each other on the internal network, not through the host.

---

## 4. Why Service Names Instead of `localhost`

Inside a container, `localhost` refers to **that container itself** — not to other containers.

If the backend used `DATABASE_URL=postgresql://...@localhost:5432/taskflow`, it would look for PostgreSQL inside the backend container, find nothing, and crash.

Because all containers are on `taskflow-net`, Docker DNS resolves `postgres` → the IP of the postgres container. So `postgresql://taskflow_user:pass@postgres:5432/taskflow` works perfectly.

---

## 5. Healthchecks and `depends_on` Conditions

A **healthcheck** tells Docker how to test if a service is truly ready (not just started):

```yaml
# postgres healthcheck
test: ["CMD-SHELL", "pg_isready -U taskflow_user -d taskflow"]
interval: 5s
retries: 10
```

`depends_on` with `condition: service_healthy` makes Docker **wait** until the dependency is healthy before starting the dependent service:

```yaml
backend:
  depends_on:
    postgres:
      condition: service_healthy   # waits for pg_isready to pass
    redis:
      condition: service_healthy   # waits for redis-cli ping to pass
```

Without this, the backend would start immediately, try to connect to PostgreSQL which is still initializing, and crash. Our backend also has its own retry loops (30 attempts) as a second safety net.

---

## 6. How Named Volumes Give Persistence

```yaml
volumes:
  postgres_data:        # named volume managed by Docker

services:
  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

`docker compose down` stops and removes containers but **leaves named volumes intact**. The data files stored in `/var/lib/postgresql/data` persist on the host in Docker's volume storage (`/var/lib/docker/volumes/` on Linux).

Only `docker compose down -v` removes volumes. This is why our persistence test works: down → up → data still there.

---

## 7. How Environment Variables and Secrets Are Handled

**Local development (`.env` file):**
- `.env` is loaded by Docker Compose automatically
- Variables are substituted into `docker-compose.yml` as `${VAR}`
- `.env` is in `.gitignore` — never committed

**CI (GitHub Actions):**
- The workflow creates a `.env` file at runtime: `cat > .env << 'EOF' ... EOF`
- No secrets are stored in the repo

**CD (GitHub Actions + Docker Hub):**
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, `POSTGRES_PASSWORD` are stored as **GitHub Encrypted Secrets**
- Accessed as `${{ secrets.SECRET_NAME }}` — never logged
- The deploy `.env` is created at runtime in the workflow

**Rule:** No passwords, tokens, or secrets are committed in any file. The deploy compose uses `${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}` — if the variable is missing, Compose exits with an error rather than using an empty value.

---

## 8. What the CD Workflow Does Stage by Stage

| Step | What happens |
|---|---|
| **Checkout** | Pulls your repo code onto the GitHub Actions runner |
| **Validate secrets** | Fails fast if `DOCKERHUB_USERNAME` or `DOCKERHUB_TOKEN` are missing |
| **Buildx setup** | Installs Docker Buildx for multi-platform builds |
| **Docker Hub login** | `docker login` using the secret token |
| **Build & push backend** | Builds `./backend/Dockerfile`, pushes `vivvvekk/taskflow-backend:latest` and `:sha` |
| **Build & push frontend** | Builds `./frontend/Dockerfile`, pushes `vivvvekk/taskflow-frontend:latest` and `:sha` |
| **Create .env** | Writes deployment env vars to `.env` on the runner |
| **Validate deploy compose** | Checks no `build:` key exists in `docker-compose.deploy.yml` |
| **Pull images** | `docker compose -f docker-compose.deploy.yml pull` |
| **Deploy** | `docker compose -f docker-compose.deploy.yml up -d` |
| **Health check** | Polls `http://localhost:3000/health` up to 40 times (120 s) |
| **Frontend check** | Curls `http://localhost:8080/` |
| **API tests** | Runs Jest tests in `tests/` against the live deployment |
| **Cleanup** | `down -v` removes containers and test volumes |

---

## 9. 10 Likely Viva Questions & Short Answers

**Q1: What is Docker and why do we use it?**  
Docker packages an application and all its dependencies into a portable container that runs identically on any machine, eliminating "works on my machine" problems.

**Q2: What is the difference between `docker-compose.yml` and `docker-compose.deploy.yml`?**  
`docker-compose.yml` uses `build:` to build images from local Dockerfiles — for local development. `docker-compose.deploy.yml` uses `image:` to pull pre-built images from Docker Hub — for production deployment. No `build:` key is allowed in the deploy file.

**Q3: Why does the backend `Dockerfile` run as the `node` user?**  
Running as root inside a container is a security risk. If an attacker exploits the app, they'd have root inside the container. The `node` user (uid 1000) limits the blast radius. `node:20-alpine` ships this user by default.

**Q4: What does `npm ci --omit=dev` do?**  
`npm ci` is a clean install that strictly follows `package-lock.json` (reproducible). `--omit=dev` skips `devDependencies`, which are tools like Vite and test runners — not needed in production, keeping the image smaller.

**Q5: What is a Docker volume and how is it different from a bind mount?**  
A named volume (`postgres_data`) is managed by Docker and stored in Docker's internal storage. A bind mount maps a host path directly (e.g., `./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql`). Volumes are preferred for databases because they're portable and Docker manages their lifecycle.

**Q6: What happens when you run `docker compose down` vs `docker compose down -v`?**  
`down` stops and removes containers and networks, but keeps named volumes. `down -v` also removes volumes, wiping the database. You'd use `-v` to start fresh, but NOT in production.

**Q7: What is the purpose of the `healthcheck` in the postgres service?**  
It runs `pg_isready` periodically. When it passes, Docker marks the container `healthy`. The backend's `depends_on: condition: service_healthy` waits for this before starting — preventing connection errors during startup.

**Q8: How does nginx serve a React SPA without getting 404 on page refresh?**  
The `try_files $uri $uri/ /index.html;` directive tells nginx: if the requested file doesn't exist on disk, serve `index.html` instead. React Router then handles the route client-side.

**Q9: Why do we use `${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}` in the deploy compose?**  
The `:?` syntax makes Docker Compose exit with an error message if the variable is unset or empty. This prevents deploying with an empty password by accident — a fail-safe.

**Q10: What secrets are needed for the CD pipeline and where are they stored?**  
Three secrets: `DOCKERHUB_USERNAME` (your Docker Hub username), `DOCKERHUB_TOKEN` (a Docker Hub access token with Read/Write), and `POSTGRES_PASSWORD` (database password). They are stored as **GitHub Encrypted Secrets** in the fork's Settings → Secrets and variables → Actions. They are injected as environment variables in the workflow and never appear in logs.
