# ---------------------------------------------------------------
# TaskFlow frontend (React + Vite, served by Nginx)
# Build context: ./frontend
# Multi-stage build: Node builds the static files, Nginx serves them.
# ---------------------------------------------------------------

# ---------- Stage 1: build the React application ----------
FROM node:22-alpine AS build

WORKDIR /app

# Manifests first for better layer caching
COPY package*.json ./
RUN npm install --no-audit --no-fund

# Source code, then production build (output goes to /app/dist)
COPY . .
RUN npm run build

# ---------- Stage 2: serve the production build with Nginx ----------
FROM nginx:stable-alpine

# nginx.conf serves the SPA and proxies /api/ and /health to http://backend:3000
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=5 \
  CMD wget -qO- http://127.0.0.1:80/ > /dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
