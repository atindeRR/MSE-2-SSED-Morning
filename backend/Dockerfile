
# Use Node.js 20 Alpine as the base image
FROM node:20-alpine

# Set working directory inside the container
WORKDIR /app

# Copy package configuration files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend application source code
COPY --chown=node:node . .

# Run the application as a non-root user
USER node

# Backend listens on port 3000
EXPOSE 3000

# Start the backend application
CMD ["npm", "start"]
