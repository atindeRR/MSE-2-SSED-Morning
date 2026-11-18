# syntax=docker/dockerfile:1

# Build React/Vite with development dependencies in a separate Node stage.
FROM node:24.22.3-alpine3.23@sha256:3946fb783fdce8a2812136ea694bc95c698c4f4096f3fd18568dc27a8ac389dc AS build
WORKDIR /app

# Copy dependency manifests first so source edits can reuse the install layer.
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --include=dev --no-audit --no-fund

COPY . .
RUN npm run build

# The runtime contains only Nginx, its configuration, and built static assets.
FROM nginx:1.30.6-alpine@sha256:901e593c95dc85f5a729f5765516321366ef4ac401821431d408897e95287d0a AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist/ /usr/share/nginx/html/

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["wget", "-q", "--spider", "-T", "3", "http://127.0.0.1:80/"]

CMD ["nginx", "-g", "daemon off;"]
