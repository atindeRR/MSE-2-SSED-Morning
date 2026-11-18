# Backend Dockerfile for TaskFlow
# Multi-stage build not needed for Node.js backend - single stage is appropriate

# Use pinned Node.js LTS Alpine image for smaller size and security
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dumb-init for proper signal handling (pinned version)
RUN apk add --no-cache dumb-init=1.2.5-r3

# Copy package files first for better layer caching
COPY package*.json ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy application source code
COPY src ./src

# Use existing node user (UID 1000) from base image
# Change ownership of app directory to node user
RUN chown -R node:node /app

# Switch to non-root user (UID 1000 = node user in base image)
USER 1000

# Expose the application port
EXPOSE 3000

# Health check using the application's /health endpoint
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/health || exit 1

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", "src/server.js"]