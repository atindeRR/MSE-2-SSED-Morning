# ─────────────────────────────────────────────
# Production Dockerfile – TaskFlow Backend
# ─────────────────────────────────────────────
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency manifests first to leverage Docker layer caching.
# The wildcard ensures package-lock.json is included only when present.
COPY package.json package-lock.json* ./

# Install production dependencies only (no devDependencies).
RUN npm install --omit=dev

# Copy application source and all required runtime files.
COPY src/ ./src/

# Copy database initialisation scripts (e.g. init.sql used by postgres).
COPY db/ ./db/

# ── Runtime environment variables ─────────────────────────────────────────────
# No sensitive values are hardcoded here.
# All secrets/credentials must be supplied at runtime via the environment
# (docker run -e, docker-compose environment block, or a secrets manager).
#
# Required at runtime:
#   DATABASE_URL  – e.g. postgresql://user:pass@host:5432/dbname
#   REDIS_URL     – e.g. redis://redis:6379
#   JWT_SECRET    – long random string
#
# Optional (defaults shown):
ENV PORT=3000 \
    NODE_ENV=production

# Expose the port the Express server listens on.
EXPOSE 3000

# Graceful shutdown is handled inside server.js (SIGTERM / SIGINT).
CMD ["npm", "start"]
