# TaskFlow API: Node.js + Express
FROM node:22-alpine

ENV NODE_ENV=production
WORKDIR /app

# Install production dependencies first so this layer is cached
# until package.json changes.
COPY --chown=1000:1000 package*.json ./
RUN npm install --omit=dev --no-audit --no-fund \
    && npm cache clean --force

# Application source (db/init.sql is mounted into PostgreSQL by Compose).
COPY --chown=1000:1000 src ./src

# Configuration comes from the environment at runtime:
# PORT, DATABASE_URL, REDIS_URL, JWT_SECRET
# Run as the built-in unprivileged "node" user (uid 1000).
USER 1000:1000
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:' + (process.env.PORT || 3000) + '/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
