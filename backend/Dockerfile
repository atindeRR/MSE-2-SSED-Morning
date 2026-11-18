# Stage 1: Build dependencies
FROM node:20.18-alpine AS builder

WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev

# Stage 2: Production runtime
FROM node:20.18-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./
COPY src ./src

USER 1000:1000

EXPOSE 3000

CMD ["node", "src/server.js"]
