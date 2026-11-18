
# Use Node.js LTS Alpine image
FROM node:22-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend source code
COPY src ./src
COPY db ./db

# Backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
