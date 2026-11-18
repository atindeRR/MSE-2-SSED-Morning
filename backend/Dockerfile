# ---------- TaskFlow backend (Node.js + Express) ----------
# Small, pinned LTS base image (alpine keeps the image light)
FROM node:22-alpine

# Production mode: npm skips devDependencies, Express runs optimised
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# Copy only the manifest first so the dependency layer is cached
# and is rebuilt only when package.json changes
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund \
    && npm cache clean --force

# Copy the application source, owned by the non-root "node" user
COPY --chown=node:node src ./src
COPY --chown=node:node db ./db

# Never run the app as root
USER node

EXPOSE 3000

# Container-level health check against the app's /health endpoint
# (checks the API, PostgreSQL and Redis together)
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1

# Exec form so node is PID 1 and receives SIGTERM for graceful shutdown
CMD ["node", "src/server.js"]
