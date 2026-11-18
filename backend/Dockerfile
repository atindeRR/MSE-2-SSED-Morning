# Use official Node.js 20 Alpine base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Configure default environment variables
ENV NODE_ENV=production \
    PORT=3000

# Copy package manifests first for efficient layer caching
COPY package.json ./

# Install production dependencies
RUN npm install --omit=dev && npm cache clean --force

# Copy application source files with non-root ownership
COPY --chown=1000:1000 . .

# Run as non-root user (node uid:gid 1000:1000)
USER 1000:1000

# Expose backend port
EXPOSE 3000

# Start backend application
CMD ["node", "src/server.js"]

