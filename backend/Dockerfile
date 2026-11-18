# Production Dockerfile for Node.js Express backend
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Configure production environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Copy dependency manifests
COPY package*.json ./

# Install dependencies and clean npm cache
RUN npm install --omit=dev && npm cache clean --force

# Copy application source code with proper ownership
COPY --chown=node:node . .

# Run as non-root user for security best practices
USER node

# Expose backend service port
EXPOSE 3000

# Start backend application
CMD ["node", "src/server.js"]
