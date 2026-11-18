FROM node:22-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund

COPY src/ ./src/

USER 1000:1000
EXPOSE 3000
CMD ["node", "src/server.js"]
