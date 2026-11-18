# Stage 1: Build stage
FROM node:20.18.0-alpine3.20 AS build

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code and build production assets
COPY . .
RUN npm run build

# Stage 2: Production runtime stage
FROM nginx:1.27.2-alpine

# Copy built frontend assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
