# ---------- Stage 1: build the React (Vite) application ----------
FROM node:22-alpine AS build

WORKDIR /app

# Copy only the manifests first so this layer is cached until dependencies change
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- Stage 2: serve the static build with Nginx ----------
FROM nginx:1.28-alpine AS runtime

# Site config: serves the SPA and proxies /api and /health to the backend service
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
  CMD ["wget", "-q", "--spider", "http://127.0.0.1/"]

CMD ["nginx", "-g", "daemon off;"]
