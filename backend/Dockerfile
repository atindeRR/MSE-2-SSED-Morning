FROM node:20-alpine

WORKDIR /app

# Copy package files first so Docker caches the npm install layer
COPY package*.json ./
RUN npm ci --omit=dev

COPY . .

ENV NODE_ENV=production
ENV PORT=5000

EXPOSE 5000

# Run as the non-root "node" user (best practice)
USER node

CMD ["npm", "start"]