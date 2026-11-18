# Multi-stage build for React + Vite Frontend

# Stage 1: Build stage
FROM node:20.18.1-alpine3.20 AS builder

WORKDIR /app

# Copy dependency specifications first to leverage Docker layer caching
COPY package*.json ./

# Install all dependencies required for building the application
RUN npm install

# Copy application source code and configuration files
COPY index.html vite.config.js ./
COPY src/ ./src/

# Build static assets for production
RUN npm run build

# Stage 2: Production web server
FROM nginx:1.27.2-alpine

# Copy built static assets from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration for SPA routing and API reverse proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
