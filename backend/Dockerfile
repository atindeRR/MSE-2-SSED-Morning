# syntax=docker/dockerfile:1

# Install the existing locked production dependencies in a cached stage.
FROM node:24.22.3-alpine3.23@sha256:3946fb783fdce8a2812136ea694bc95c698c4f4096f3fd18568dc27a8ac389dc AS dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev --no-audit --no-fund

# Keep dependency-install cache and build-stage files out of the runtime.
FROM node:24.22.3-alpine3.23@sha256:3946fb783fdce8a2812136ea694bc95c698c4f4096f3fd18568dc27a8ac389dc AS runtime
ENV NODE_ENV=production \
    PORT=3000
WORKDIR /app
COPY --chown=node:node package.json package-lock.json ./
COPY --from=dependencies --chown=node:node /app/node_modules ./node_modules
COPY --chown=node:node src/ ./src/

USER 1000:1000
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["node", "--input-type=module", "-e", "try { const response = await fetch('http://127.0.0.1:' + (process.env.PORT || 3000) + '/health', { signal: AbortSignal.timeout(3000) }); const body = await response.json(); process.exit(response.status === 200 && body.status === 'ok' && body.postgres === 'ok' && body.redis === 'ok' ? 0 : 1); } catch { process.exit(1); }"]

# This is the exact Node command behind package.json's existing start script.
# Exec form delivers Docker termination signals directly to the application.
CMD ["node", "src/server.js"]
