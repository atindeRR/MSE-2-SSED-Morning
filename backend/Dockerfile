# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package file
COPY package.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Use non-root node user
USER node

# Backend port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]