
# Stage 1: Build React application
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package configuration
COPY package.json ./

# Install dependencies
RUN npm install --no-audit --no-fund

# Copy frontend source
COPY . .

# Build production files
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:1.29-alpine

# Copy production build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

