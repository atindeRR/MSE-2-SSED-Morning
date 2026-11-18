
# Use lightweight Node.js image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy package configuration
COPY package.json ./

# Install production dependencies
RUN npm install --omit=dev --no-audit --no-fund

# Copy application source code
COPY --chown=node:node src/ ./src/
COPY --chown=node:node db/ ./db/

# Use non-root user
USER 1000

# Backend port
EXPOSE 3000

# Start application
CMD ["npm", "start"]

