
# Use Node.js Alpine image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY --chown=node:node . .

# Run application as non-root user
USER node

# Backend port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
