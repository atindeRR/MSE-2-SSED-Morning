FROM node:20.18.1-alpine
ENV NODE_ENV=production
WORKDIR /app

# Copy only package.json first so the dependency layer is cached
COPY package.json ./
RUN npm install --omit=dev && npm cache clean --force

# Copy application source last (changes most often)
COPY --chown=node:node src ./src

# Run as the non-root user that ships with the node image
USER node
EXPOSE 3000

# DATABASE_URL, REDIS_URL, JWT_SECRET and PORT are supplied at runtime (never baked in)
CMD ["node", "src/server.js"]
