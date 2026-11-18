
# Use Node.js base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Set environment variables
ENV NODE_ENV=production

# Backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
