FROM node:22-alpine

# Set working directory
WORKDIR /app

# NODE_ENV=production tells npm ci to skip devDependencies
ENV NODE_ENV=production

# Copy dependency manifests first for better layer caching
COPY package.json package-lock.json* ./

# Install production dependencies only
RUN npm ci --omit=dev

# Copy application source
COPY src ./src

# The backend listens on the PORT env variable (default 3000 in config.js)
EXPOSE 3000

# Start the Express server (ESM entry point)
CMD ["node", "src/server.js"]
