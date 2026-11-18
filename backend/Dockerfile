# ---- Backend Dockerfile ----
FROM node:18-alpine

WORKDIR /app

# Copy dependency files first for layer caching
COPY package.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code
COPY . .

# Expose backend port
EXPOSE 3000

# Start the application
CMD ["node", "src/server.js"]
