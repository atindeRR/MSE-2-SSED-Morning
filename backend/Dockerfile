
# Use Node.js Alpine image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install production dependencies only
RUN npm install --omit=dev

# Copy backend application code
COPY . .

# Expose backend port
EXPOSE 3000

# Start the Express application
CMD ["npm", "start"]
