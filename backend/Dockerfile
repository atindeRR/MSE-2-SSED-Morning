FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./

RUN npm install --omit=dev

COPY src/ ./src/
COPY db/ ./db/

USER 1000:1000

EXPOSE 3000

CMD ["node", "src/server.js"]
