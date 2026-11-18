
# Use Node.js base image
FROM node:22-alpine

WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend source code
COPY --chown=node:node . .

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose backend port
EXPOSE 3000

# Run as non-root user
USER node

# Start backend
CMD ["npm", "start"]
