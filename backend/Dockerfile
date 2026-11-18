
# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend source code
COPY . .

# Backend listens on port 3000
EXPOSE 3000

# Start the backend server
CMD ["npm", "start"]
