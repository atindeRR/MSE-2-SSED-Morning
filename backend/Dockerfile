
# Use Node.js Alpine base image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source code
COPY --chown=node:node . .

# Use non-root user
USER node

# Backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
