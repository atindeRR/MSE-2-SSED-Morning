# Phase 3 - Backend Dockerization

## Files

- `backend/Dockerfile`: locked production dependencies and a non-root Node runtime.
- `backend/package-lock.json`: generated from the existing dependency declarations.
- `backend/.dockerignore`: excludes local dependencies, credentials, and generated output.
- `tools/configure-env.mjs`: creates local runtime secrets without printing them.

## Dockerfile decisions

The same verified Node.js 24 LTS Alpine base used by the frontend build is pinned
by digest. `package.json` and its new lockfile are copied before application
source so source changes can reuse the npm installation layer.

The dependency stage runs `npm ci --omit=dev`. The runtime copies only the
production dependency tree, manifests, and original `src/` files, and runs as
the image's existing unprivileged `node` user.

`NODE_ENV=production` and `PORT=3000` are runtime defaults. PostgreSQL, Redis,
and JWT secrets are supplied externally rather than baked into the image.

The exec-form startup command is `node src/server.js`, the exact command
already used by `npm start` in the provided `package.json`. Running Node directly
allows Docker signals to reach the application's existing shutdown handlers.

The health probe requests the existing **`/health`** endpoint and checks its
actual `status`, `postgres`, and `redis` response fields. It uses Node's built-in
HTTP capabilities rather than installing curl in the application image.

## Local environment

Run from **`D:\DEVOPS\mse2`**:

```powershell
node tools/configure-env.mjs init --frontend-port 8081
```

This creates a Git-ignored `.env`, using the supplied database/user names,
generated hexadecimal database/JWT secrets, and the actual `postgres` and
`redis` service hosts. An existing `.env` is preserved. No secret values are
printed. The host-port option is for Compose/Nginx publishing; the application
itself retains backend port 3000 and Nginx port 80.

This computer's Oracle listener occupies port 8080, so the final local frontend
will use 8081. CI's frontend default remains 8080.

## Build

```powershell
docker build --progress=plain -t taskflow-backend:local ./backend
```

Expect the production dependency install and final image export to finish
successfully. Save actual output as the backend build evidence if needed.

## Runtime verification

The backend cannot be verified by starting it without its database and cache:
the existing application waits for both services before listening.

Before the permanent Compose phase, use isolated temporary PostgreSQL and Redis
containers on a dedicated Docker network, with service-name aliases `postgres`
and `redis`. Mount the supplied `backend/db/init.sql` into PostgreSQL's first-start
initialization directory. Run the backend with the local `.env` and verify:

- PostgreSQL accepts connections.
- Redis returns `PONG`.
- The backend starts as UID 1000 (`node`).
- `/health` returns HTTP 200 with all three expected fields equal to `ok`.
- Docker marks the backend healthy.
- Backend logs confirm the actual PostgreSQL and Redis connections.

The temporary verification database uses ephemeral storage and contains no
student application data. The permanent four-service Compose configuration uses
a PostgreSQL named volume. Cleanup must be limited to the temporary verification
resources and must not remove existing user database volumes.

Actual outcomes are recorded in `docs/VERIFICATION.md` after commands run.
