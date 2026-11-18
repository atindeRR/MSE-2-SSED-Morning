
# Stage 1: Build the React application
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Build production files
RUN npm run build


# Stage 2: Serve using Nginx
FROM nginx:1.27-alpine

# Copy production build
COPY --from=builder /app/dist /usr/share/nginx/html

# Configure Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
