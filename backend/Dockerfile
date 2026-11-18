# Stage 1: Dependency resolution and production installation
FROM node:20-alpine AS dependencies

WORKDIR /app

# Copy package manifests
COPY package*.json ./

# Install only production dependencies
RUN npm install --omit=dev && npm cache clean --force

# Stage 2: Final lightweight production image
FROM node:20-alpine

WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy node_modules from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy package.json and application source code
COPY package*.json ./
COPY src/ ./src/

# Run as non-root user (node user provided by base image)
USER node

# Expose backend port
EXPOSE 3000

# Start backend server
CMD ["node", "src/server.js"]
