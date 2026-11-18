# Production Dockerfile for Node.js + Express Backend

FROM node:20.18.1-alpine3.20

# Set working directory
WORKDIR /app

# Set production environment variables
ENV NODE_ENV=production \
    PORT=3000

# Copy package manifests first for optimal Docker layer caching
COPY package*.json ./

# Install only production dependencies and clean cache
RUN npm install --omit=dev && npm cache clean --force

# Copy application source code and database initialization files with non-root ownership
COPY --chown=1000:1000 src/ ./src/
COPY --chown=1000:1000 db/ ./db/

# Switch to non-root node user (UID 1000:1000) for security compliance
USER 1000:1000

# Expose backend service port
EXPOSE 3000

# Start backend application using npm start as configured in package.json
CMD ["npm", "start"]
