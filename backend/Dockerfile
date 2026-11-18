FROM node:20.18.0-alpine3.20

WORKDIR /app

# Copy dependency files first for caching
COPY package.json package-lock.json ./

# Install production dependencies
RUN npm ci --omit=dev && npm cache clean --force

# Copy application source and db files
COPY db ./db
COPY src ./src

# Run as non-root user (node user UID:GID 1000:1000)
USER 1000:1000

# Expose backend service port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]
