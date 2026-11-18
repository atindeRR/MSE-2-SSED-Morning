# Use Node.js 20 Alpine as base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend source code
COPY . .

# Expose backend port
EXPOSE 3000

# Start the backend server
CMD ["npm", "start"]
