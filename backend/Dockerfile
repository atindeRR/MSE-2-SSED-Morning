
# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY --chown=node:node . .

# Switch to non-root user
USER node

# Backend listens on port 3000
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
