# Use Node.js 20
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Backend port
EXPOSE 3000

# Start backend
CMD ["npm", "start"]