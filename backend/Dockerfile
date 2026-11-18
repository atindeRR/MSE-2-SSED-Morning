# Backend Dockerfile for TaskFlow
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package definition files
COPY package*.json ./

# Install only production dependencies and clean cache
RUN npm install --omit=dev && npm cache clean --force

# Copy application source code with appropriate ownership
COPY --chown=node:node . .

# Expose backend API port
EXPOSE 3000

# Run container as non-root user
USER node

# Start the application server
CMD ["node", "src/server.js"]
