# ---------- Stage 1: install production dependencies ----------
FROM node:22-alpine AS deps

WORKDIR /app

# Copy only the manifests first so this layer is cached until dependencies change
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# ---------- Stage 2: runtime image ----------
FROM node:22-alpine AS runtime

# Non-secret defaults. DATABASE_URL, REDIS_URL and JWT_SECRET are supplied
# at runtime (docker compose / .env) and are never baked into the image.
ENV NODE_ENV=production \
    PORT=3000

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --chown=node:node package.json ./
COPY --chown=node:node src ./src

# Run as the unprivileged "node" user (uid/gid 1000) from the official image
USER 1000:1000

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:' + (process.env.PORT || 3000) + '/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
