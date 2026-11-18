
FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./

# Install dependencies
RUN npm install --omit=dev

# Copy source code with correct ownership
COPY --chown=node:node . .

# Run as non-root user
USER node

EXPOSE 3000

CMD ["npm", "start"]
