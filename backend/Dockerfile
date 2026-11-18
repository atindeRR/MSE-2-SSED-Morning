# ---- Stage 1: Dependencies ----
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

# ---- Stage 2: Production image ----
FROM node:20-alpine
WORKDIR /app

# Copy installed dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy application source
COPY . .

# Expose backend port
EXPOSE 3000

# Use environment variables for configuration (never hardcode)
ENV PORT=3000

# Start the application
CMD ["node", "src/server.js"]
