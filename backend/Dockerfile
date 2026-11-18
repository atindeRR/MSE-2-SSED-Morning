# Backend: Node.js + Express API
FROM node:24.22.3-alpine3.24

ENV NODE_ENV=production
WORKDIR /app

# Install dependencies first (better layer caching)
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund \
 && npm cache clean --force

# Copy application source
COPY src ./src

# Run as the non-root "node" user (uid 1000) that ships with the image
USER 1000

# Config comes from environment variables (DATABASE_URL, REDIS_URL, JWT_SECRET, PORT)
EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD ["wget", "-qO-", "http://127.0.0.1:3000/health"]

CMD ["node", "src/server.js"]
