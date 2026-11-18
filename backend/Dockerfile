
# Use Node.js LTS Alpine image
FROM node:22-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev --no-audit --no-fund

# Copy backend source code
COPY src/ ./src/
COPY db/ ./db/

# Set production environment
ENV NODE_ENV=production

# Backend listens on port 3000
EXPOSE 3000

# Run as non-root user for better security
USER node

# Start the backend server
CMD ["npm", "start"]
