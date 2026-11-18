
# Use Node.js Alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Backend port
EXPOSE 3000

# Start backend application
CMD ["npm", "start"]
