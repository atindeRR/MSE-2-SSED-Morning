# Repository Analysis and Implementation Plan

## 1. Verified repository identity

- Course: Software Engineering and DevOps (AI310B), MSE-2 Morning.
- Application: TaskFlow.
- Working directory: `D:\DEVOPS\mse2`.
- Personal fork: https://github.com/adidev001/MSE-2-SSED-Morning
- Starter: https://github.com/atindeRR/MSE-2-SSED-Morning
- Branch: `main`.
- Imported starter commit: `810be2292c988a4e10c181f55c50675286dd9127`.

The fork's public GitHub metadata confirms that its parent is the specified
starter. The existing Git history was imported directly into the working
directory using `git pull --ff-only origin main`.

## 2. Tracked starter structure

This is the starter structure inspected before implementation:

```text
.
|-- .github/
|   `-- workflows/
|       |-- cd.yml
|       `-- ci.yml
|-- backend/
|   |-- .dockerignore
|   |-- Dockerfile                 (empty in starter)
|   |-- package.json
|   |-- db/
|   |   `-- init.sql
|   `-- src/
|       |-- app.js
|       |-- auth.js
|       |-- config.js
|       |-- db.js
|       |-- redis.js
|       `-- server.js
|-- frontend/
|   |-- .dockerignore
|   |-- Dockerfile                 (empty in starter)
|   |-- index.html
|   |-- nginx.conf
|   |-- package.json
|   |-- vite.config.js
|   `-- src/
|       |-- main.jsx
|       `-- style.css
|-- tests/
|   |-- api.test.js
|   |-- jest.config.js
|   |-- package.json
|   `-- package-lock.json
|-- .env.example
|-- .gitignore
`-- README.md
```

Neither Compose file is supplied. Frontend and backend lockfiles are absent;
the test directory already has a lockfile.

## 3. Frontend configuration

Source of truth: `frontend/package.json`, `frontend/vite.config.js`,
`frontend/nginx.conf`, and `frontend/src/main.jsx`.

- React and React DOM: `^18.3.1`.
- Vite: `^5.4.11`; React Vite plugin: `^4.3.4`.
- Development script: `vite --host 0.0.0.0`.
- Production build script: `vite build` (`npm run build`).
- Production output: Vite's `dist` directory.
- Nginx container port: **80**, explicitly set in the supplied configuration.
- Host port required by both workflows: **8080**.
- API base used by the browser: the relative path **`/api`**.
- Nginx API upstream: **`backend:3000`**, preserving the `/api/` prefix.
- Nginx also forwards `/health` to the existing backend health endpoint.
- The supplied `try_files` rule supports React single-page routing.

The production build needs development dependencies because Vite and its plugin
are in `devDependencies`. They belong in the build stage, not the runtime image.

## 4. Backend configuration

Source of truth: `backend/package.json` and `backend/src/`.

- Express: `^4.21.2`.
- Other existing dependencies: `bcryptjs`, `cors`, `jsonwebtoken`, `pg`, and
  `redis`.
- Production start: **`npm start`**, which runs **`node src/server.js`**.
- Development start: `node --watch src/server.js`.
- Listening address: **`0.0.0.0`**.
- Listening port: `PORT`, defaulting to **3000**.
- Startup waits for PostgreSQL and Redis before opening the HTTP listener.
- The application does not contain a database migration/startup schema script.
  PostgreSQL must initialize the provided SQL file during first startup.

### Existing routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Check PostgreSQL and Redis |
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Authenticate and return a JWT |
| GET | `/api/tasks` | List the authenticated user's tasks |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/:id` | Update a task |
| DELETE | `/api/tasks/:id` | Delete a task |

The successful health response defined by the source is:

```json
{"status":"ok","postgres":"ok","redis":"ok"}
```

This is an expected response, not a recorded deployment result.

## 5. Database and cache

`backend/src/db.js` creates a PostgreSQL pool from `DATABASE_URL`.
`backend/db/init.sql` creates the `users` and `tasks` tables and a user-task
index. The Compose database service must mount this script read-only under
PostgreSQL's initialization directory and use a named data volume.

`backend/src/redis.js` connects using `REDIS_URL`. Task lists are cached under
`tasks:user:<userId>` for **30 seconds**. Creating, updating, or deleting a task
invalidates that user's cached list. Successful list responses report their
source as `postgres` or `redis-cache`.

## 6. Actual environment variables

| Variable | Consumer | Starter value or purpose |
|---|---|---|
| `PORT` | Backend | `3000` |
| `DATABASE_URL` | Backend | PostgreSQL URL using `postgres:5432` |
| `REDIS_URL` | Backend | `redis://redis:6379` |
| `JWT_SECRET` | Backend | JWT signing secret; replace the placeholder |
| `POSTGRES_DB` | PostgreSQL | `taskflow` |
| `POSTGRES_USER` | PostgreSQL | `taskflow_user` |
| `POSTGRES_PASSWORD` | PostgreSQL | Local secret; GitHub Actions secret for CD |
| `DOCKERHUB_USERNAME` | Deployment Compose/CD | Required for registry image names |

`DOCKERHUB_USERNAME` is required by the supplied CD workflow but is not yet
included in the starter `.env.example`. Docker Hub access tokens belong in
Docker's authentication flow and GitHub repository secrets, not in application
images or tracked files.

## 7. Planned communication

```text
Browser -> localhost:8080 -> frontend (Nginx :80)
                              |
                              +-- /api/* -> backend:3000
                              +-- /health -> backend:3000/health
                                                |
                                                +-- postgres:5432
                                                `-- redis:6379
```

Compose service names provide DNS inside the Docker network. `localhost` is
appropriate for host browser requests and a container's own health probe, but
not for backend connections to the PostgreSQL or Redis containers.

## 8. Existing workflow findings

### CD: `.github/workflows/cd.yml`

The existing workflow runs on pushes to `main` and manual dispatch. It already
checks out the repository, configures Buildx, authenticates to Docker Hub, builds
and pushes both images, pulls and starts deployment Compose, verifies HTTP
responses, and runs the supplied API tests.

Required adjustments identified from the actual file:

1. Align image tags and summary references with the examination's required
   `<username>/frontend` and `<username>/backend` names. The starter uses
   `taskflow-frontend` and `taskflow-backend`.
2. Use `secrets.POSTGRES_PASSWORD` for CD instead of the current placeholder.
3. Supply a real runtime JWT signing secret without printing it.
4. Make frontend/backend verification output readable for required evidence.

The existing workflow structure, triggers, actions, and API tests should be
retained wherever possible.

### CI: `.github/workflows/ci.yml`

This workflow evaluates pull requests using instructor-controlled tests. It
references `scripts/check-required-files.sh` and `scripts/persistence-test.sh`
from its instructor checkout. Neither script exists in the inspected starter
commit. Instructor evaluation cannot be reported as passing without an actual
successful run and resolution of these missing evaluation files.

The README names `taskflow-docker` in its final PR instructions although the
supplied starter and fork are named `MSE-2-SSED-Morning`. Confirm the instructor's
actual target repository before creating the submission PR.

## 9. Implementation and verification plan

| Phase | Implementation | Required verification |
|---|---|---|
| 1 | Inspect and import the correct fork | Git identity, source files, real configuration |
| 2 | Frontend lockfile, multi-stage Dockerfile, Nginx configuration | Image build and static frontend response |
| 3 | Backend lockfile and non-root Dockerfile | Image build, startup, existing `/health` |
| 4 | Four-service Compose and environment templates | Compose validation, healthy service startup |
| 5 | Application and storage checks | All API tests, browser task flow, Redis cache, database persistence |
| 6 | Docker Hub `frontend` and `backend` images | Successful authenticated pushes and remote image references |
| 7 | Image-only deployment Compose | Pull, startup, API and frontend checks without builds |
| 8 | Minimal CD adjustments and repository secrets | Real successful GitHub Actions run and required stage screenshots |
| 9 | Verified submission target and final PR | Correct title, details, URLs, and available instructor evaluation |
| 10 | Evidence-based PDF | Actual readable screenshots and accurate final results |

## 10. Verified local prerequisites

The following are actual tool outputs recorded during inspection:

- Git `origin` fetch/push URL: the `adidev001` fork.
- Local `main` imported at commit `810be22`.
- Docker client and engine: **29.8.2**, Linux container context `desktop-linux`.
- Docker Compose: **v5.5.1**.
- Host Node.js: **v24.12.0**; npm: **11.6.2**.
- Official build image `node:24.22.3-alpine3.23` exists on Docker Hub.
- Official runtime image `nginx:1.30.6-alpine` exists on Docker Hub.

Inspection is complete. Application image builds, application deployment,
Docker Hub publication, CI/CD results, and screenshots must each be verified
and recorded as their respective phases are executed.
