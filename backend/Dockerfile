# Use official Node.js 20 Alpine Linux image
FROM node:20-alpine

# Set working directory inside container
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package manifests first for caching layer
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code and db init script
COPY . .

# Expose backend service port
EXPOSE 3000

# Start Express server
CMD ["node", "src/server.js"]
