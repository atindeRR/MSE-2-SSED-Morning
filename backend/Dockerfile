# syntax=docker/dockerfile:1
# ──────────────────────────────────────────────────────────────────────────────
# Stage 1: install production dependencies
# ──────────────────────────────────────────────────────────────────────────────
FROM node:22-alpine AS deps
WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev && npm cache clean --force

# ──────────────────────────────────────────────────────────────────────────────
# Stage 2: final runtime image
# ──────────────────────────────────────────────────────────────────────────────
FROM node:22-alpine AS runtime
WORKDIR /app

# Create a non-root user with explicit numeric UID/GID for security
RUN addgroup -g 1001 -S appgroup && adduser -u 1001 -S appuser -G appgroup

# Copy production node_modules from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application source
COPY src/ ./src/
COPY db/ ./db/
COPY package.json ./

# Transfer ownership to non-root user
RUN chown -R 1001:1001 /app
USER 1001

EXPOSE 3000

ENV NODE_ENV=production

CMD ["node", "src/server.js"]
