# Stage 1: Build the React application with Vite
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm install

# Copy application source code and build
COPY . .
RUN npm run build

# Stage 2: Serve the production static files with Nginx
FROM nginx:1.27-alpine

# Copy custom Nginx configuration for SPA routing and API reverse-proxying
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 (standard HTTP port inside container)
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
