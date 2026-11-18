# ---------- Stage 1: build the React (Vite) app ----------
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies first to take advantage of layer caching
COPY package*.json ./
RUN npm install --no-audit --no-fund \
    && npm cache clean --force

# Copy the source and produce the static production bundle in /app/dist
COPY . .
RUN npm run build

# ---------- Stage 2: serve the static build with Nginx ----------
FROM nginx:1.27-alpine

# Nginx config: serves the SPA and reverse-proxies /api and /health
# to the backend service (resolved by its Compose service name "backend")
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Only the compiled assets are copied; node_modules and sources stay in stage 1
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD wget -q --spider http://127.0.0.1/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
