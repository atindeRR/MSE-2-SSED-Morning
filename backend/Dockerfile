# ---------------------------------------------------------------
# TaskFlow backend (Node.js + Express)
# Build context: ./backend
# ---------------------------------------------------------------
FROM node:22-alpine

# Non-secret configuration defaults. Real values (DATABASE_URL, REDIS_URL,
# JWT_SECRET) are injected at runtime by Docker Compose, never baked in.
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

# Copy only the manifests first so the dependency layer is cached
# and only re-built when package.json changes.
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund \
    && npm cache clean --force

# Copy the application source code
COPY --chown=node:node src ./src

# Run as the unprivileged "node" user that ships with the base image
# (the app only reads from /app, it never writes there)
USER node

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
  CMD wget -qO- "http://127.0.0.1:${PORT}/health" > /dev/null || exit 1

CMD ["node", "src/server.js"]
