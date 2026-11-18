# MSE-2 | TaskFlow backend (Node.js + Express)

# Official Node.js 22 LTS image on Alpine Linux: small and with a pinned major version
FROM node:22-alpine

# Production mode: Express runs optimised and npm skips devDependencies
ENV NODE_ENV=production

# Every following instruction runs inside /app
WORKDIR /app

# Copy only the dependency manifest first, so the "npm install" layer is cached
# and re-runs only when package.json changes (not on every source code edit)
COPY package*.json ./

# Install production dependencies, then clear the npm cache to keep the image small
RUN npm install --omit=dev && npm cache clean --force

# Copy the application source code (.dockerignore keeps out node_modules, .env and tests)
COPY . .

# Non-secret default configuration; it can be overridden at runtime.
# Secrets (DATABASE_URL, JWT_SECRET) are never baked into the image; Compose injects them.
ENV PORT=3000

# Run as the unprivileged "node" user (UID 1000) that ships with the official image, not as root.
# A numeric UID is used so the user can always be resolved (hadolint rule DL3066).
USER 1000

# Document the port the API listens on
EXPOSE 3000

# Exec form: node runs as PID 1 and receives SIGTERM for a graceful shutdown
CMD ["node", "src/server.js"]
