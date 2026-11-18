# syntax=docker/dockerfile:1

# ---------- Stage 1: install production dependencies ----------
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund

# ---------- Stage 2: runtime image ----------
FROM node:20-alpine AS runtime
ENV NODE_ENV=production \
    PORT=3000
WORKDIR /app

# Run as an unprivileged user (numeric id keeps hadolint DL3066 happy) instead of root
RUN addgroup -S -g 10001 app && adduser -S -u 10001 -G app app

COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --chown=app:app package.json ./
COPY --chown=app:app src ./src

USER 10001:10001
EXPOSE 3000

CMD ["node", "src/server.js"]
