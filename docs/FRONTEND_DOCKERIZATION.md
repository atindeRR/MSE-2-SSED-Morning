# Phase 2 - Frontend Dockerization

## Files

- `frontend/Dockerfile`: production multi-stage image.
- `frontend/package-lock.json`: generated lockfile for the existing dependency
  declarations; `package.json` is the source of dependency requirements.
- `frontend/nginx.conf`: existing SPA/API routes with request-time Docker DNS.
- `frontend/.dockerignore`: excludes local dependencies, build output, Git
  metadata, and dotenv files from the frontend build context.

## Dockerfile instructions

| Instruction | Reason |
|---|---|
| `FROM node:24.22.3-alpine3.23 ... AS build` | Supported Node.js LTS build environment; the verified image digest makes the base reproducible |
| `WORKDIR /app` | Gives subsequent build commands a consistent working directory |
| `COPY package.json package-lock.json ./` | Allows dependency installation to be cached independently of source edits |
| `npm ci --include=dev` | Installs the locked dependencies, including Vite and its React plugin needed for the build |
| Cache mount on `/root/.npm` | Reuses downloaded npm packages without placing the cache in the final image |
| `COPY . .` | Copies the frontend source and configuration after dependencies are installed |
| `RUN npm run build` | Runs the existing production script and creates `/app/dist` |
| `FROM nginx:1.30.6-alpine ... AS runtime` | Starts a separate, pinned production web-server stage |
| `COPY nginx.conf ...` | Enables the provided SPA routes and backend proxy |
| `COPY --from=build /app/dist/ ...` | Copies only the production assets from the Node stage |
| `EXPOSE 80` | Documents the actual port used by the Nginx configuration; host publishing is configured separately |
| `HEALTHCHECK` | Probes the static frontend homepage without requiring the backend |
| `CMD ["nginx", "-g", "daemon off;"]` | Keeps Nginx in the foreground as the container's main process |

The final image does not contain the Node build stage or its `node_modules`.

## Nginx routing

- `/`: serves React assets, with `try_files` fallback to `index.html` for SPA
  paths.
- `/api/`: forwards the original request path and query string to the actual
  backend service at `backend:3000`.
- `/health`: forwards to the existing backend health endpoint.

The original configuration resolved `backend` while Nginx started. The updated
variable-based proxy uses Docker's embedded DNS (`127.0.0.11`) at request time,
so static frontend checks can run before the backend exists. API functionality
is verified later with the complete stack and its real PostgreSQL/Redis services.

## Build checkpoint - Screenshot 5a

Open PowerShell in **`D:\DEVOPS\mse2`** and clear the visible terminal with
**Ctrl+L** before this required evidence command:

```powershell
docker build --progress=plain -t taskflow-frontend:local ./frontend
```

This uses `frontend/` as the build context and creates the local image named
`taskflow-frontend:local`. Expect the Vite build to succeed and the final image
export/name steps to report `DONE`. Save the actual screenshot as
`evidence/screenshots/05a-frontend-build.png`.

Also capture the complete Dockerfile in VS Code as
`evidence/screenshots/02-frontend-dockerfile.png`.

## Standalone run and verification

After the build has actually succeeded, check that the test container name and
host port are available. This command publishes Nginx's container port 80 on
the workflow's expected host port 8080:

```powershell
docker run -d --name taskflow-frontend-check -p 8080:80 taskflow-frontend:local
```

Expect a real container ID, not an error. Validate its configuration:

```powershell
docker exec taskflow-frontend-check nginx -t
```

Expect `syntax is ok` and `test is successful`. Check the HTTP response:

```powershell
curl.exe --fail --silent --show-error --head http://localhost:8080/
```

Expect `HTTP/1.1 200 OK`. Open **http://localhost:8080/** to verify that the built
TaskFlow login interface loads. Account/task operations need the real backend,
which will be tested during full-stack verification.

Inspect health after allowing the configured probe to run:

```powershell
docker inspect --format "{{.State.Status}} / {{.State.Health.Status}}" taskflow-frontend-check
```

Expect `running / healthy` once the probe has succeeded. A `starting` state
requires waiting and checking again; an `unhealthy` or exited state requires
inspection of the real logs.

Remove only this temporary, stateless frontend test container before Compose
uses the same host port:

```powershell
docker stop taskflow-frontend-check
docker rm taskflow-frontend-check
```

These commands do not remove PostgreSQL volumes.

## Verification boundary

Dockerfile implementation, image-build success, static frontend accessibility,
and full application functionality are separate checks. Record each only after
actual output confirms it. No CI/CD success or Docker Hub publication is implied
by this phase.
