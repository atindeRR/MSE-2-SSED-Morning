# Stage 1: Build the React/Vite application
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package manifests first for efficient layer caching
COPY package.json ./

# Install all dependencies including devDependencies required by Vite
RUN npm install && npm cache clean --force

# Copy frontend source code
COPY . .

# Build static production assets
RUN npm run build

# Stage 2: Serve production assets with Nginx
FROM nginx:alpine

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built application assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose frontend web server port
EXPOSE 80

# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]

