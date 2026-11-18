# Multi-stage build for React frontend application

# Stage 1: Build the React application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package manifests
COPY package*.json ./

# Install dependencies and clean npm cache
RUN npm install && npm cache clean --force

# Copy application source code and build production bundle
COPY . .
RUN npm run build

# Stage 2: Serve the production build using Nginx
FROM nginx:1.27-alpine

# Copy built assets to Nginx default html folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose container port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
