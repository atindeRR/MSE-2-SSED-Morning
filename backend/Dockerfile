# Use an appropriate Node.js base image
FROM node:18-alpine
WORKDIR /app

# Follow Docker best practices by setting the environment to production
ENV NODE_ENV=production

# Copy package files and install the required dependencies
COPY package*.json ./
# Clean the cache to keep the image lightweight (best practice)
RUN npm install --omit=dev && npm cache clean --force

# Copy the rest of the application source code
COPY . .

# Expose the backend port (standard for Node/Express, will be mapped in Compose)
EXPOSE 5000

# Configure the application startup command
CMD ["npm", "start"]