# ---- Backend: Node.js + Express API ----
FROM node:20-alpine

# Production mode: skips devDependencies, faster Express
ENV NODE_ENV=production

WORKDIR /app

# Copy only package files first -> Docker caches the npm install layer
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

# Copy the application source (node_modules/.env excluded by .dockerignore)
COPY . .

# Never run as root: uid 1000 is the built-in "node" user of the image
USER 1000

EXPOSE 3000

# Container-level health check (busybox wget exists in alpine)
HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD ["wget", "-qO-", "http://127.0.0.1:3000/health"]

CMD ["node", "src/server.js"]
