
# Use Node.js base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend source code
COPY --chown=node:node src ./src

# Set production environment
ENV NODE_ENV=production

# Use non-root user
USER node

# Expose backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
