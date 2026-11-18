# Use official Node.js LTS Alpine image for smaller size
FROM node:20-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Expose the backend port
EXPOSE 3000

# Use non-root user for security
USER node

# Start the application
CMD ["node", "src/server.js"]
