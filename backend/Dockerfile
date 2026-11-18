# Node.js backend – production image
FROM node:20-alpine

WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm install

# Copy application source code
COPY . .

# Expose backend port (matches PORT env variable default)
EXPOSE 3000

# Use environment variables for configuration (never hardcode secrets)
ENV NODE_ENV=production

CMD ["node", "src/server.js"]
