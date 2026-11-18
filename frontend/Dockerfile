
# Stage 1: Build React application
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependency configuration
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Build production files
RUN npm run build


# Stage 2: Serve using Nginx
FROM nginx:alpine

# Remove default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy production build from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

services:
  postgres:
    image: postgres:16-alpine
    container_name: taskflow-deploy-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-taskflow}
      POSTGRES_USER: ${POSTGRES_USER:-taskflow_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backend/db/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - taskflow-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: taskflow-deploy-redis
    restart: unless-stopped
    networks:
      - taskflow-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    image: ${DOCKERHUB_USERNAME:?Set DOCKERHUB_USERNAME in .env}/taskflow-backend:latest
    container_name: taskflow-deploy-backend
    restart: unless-stopped
    environment:
      PORT: 3000
      DATABASE_URL: postgresql://${POSTGRES_USER:-taskflow_user}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB:-taskflow}
      REDIS_URL: redis://redis:6379
      JWT_SECRET: ${JWT_SECRET:?Set JWT_SECRET in .env}
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - taskflow-network
    healthcheck:
      test:
        - CMD
        - node
        - -e
        - "fetch('http://127.0.0.1:3000/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"
      interval: 15s
      timeout: 5s
      retries: 5
      start_period: 20s

  frontend:
    image: ${DOCKERHUB_USERNAME:?Set DOCKERHUB_USERNAME in .env}/taskflow-frontend:latest
    container_name: taskflow-deploy-frontend
    restart: unless-stopped
    ports:
      - "8080:80"
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - taskflow-network

volumes:
  postgres_data:

networks:
  taskflow-network:
    driver: bridge
