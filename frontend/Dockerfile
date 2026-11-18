
# Stage 1: Build React + Vite frontend
FROM node:20.18.0-alpine3.20 AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock*.json ./

RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy source code
COPY . .

# Build production files
RUN npm run build


# Stage 2: Production Nginx server
FROM nginxinc/nginx-unprivileged:1.27.2-alpine

# Configure Nginx
COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf

# Copy React + Vite production build
COPY --chown=101:101 --from=builder /app/dist /usr/share/nginx/html

# Nginx listens on port 8080
EXPOSE 8080

# Frontend health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
