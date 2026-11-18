
# Use lightweight Node.js image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source
COPY src ./src

# Set production environment
ENV NODE_ENV=production

# Run as non-root user
USER node

# Backend application port
EXPOSE 3000

# Start Express server
CMD ["npm", "start"]
