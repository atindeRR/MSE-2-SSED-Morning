# Stage 1: Build the React application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package definition files
COPY package*.json ./

# Install build and runtime dependencies
RUN npm install && npm cache clean --force

# Copy frontend source code
COPY . .

# Build production bundle
RUN npm run build

# Stage 2: Serve production assets with Nginx
FROM nginx:1.27-alpine

# Copy custom Nginx reverse proxy configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy compiled static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose web server HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
