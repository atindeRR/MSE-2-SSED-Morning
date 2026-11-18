# ---------- Backend: Node.js + Express API ----------
FROM node:22.11.0-alpine3.20

ENV NODE_ENV=production
WORKDIR /app

# copy manifests first so the dependency layer is cached between builds
COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund && npm cache clean --force

# application source (configuration comes from environment variables at runtime)
COPY src ./src
COPY db ./db

# run as the unprivileged user that ships with the node image
USER node
EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=3s --start-period=20s --retries=5 \
  CMD wget -qO- http://127.0.0.1:3000/health || exit 1

CMD ["node", "src/server.js"]
