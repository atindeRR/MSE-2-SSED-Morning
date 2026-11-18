FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production \
    PORT=3000

COPY package*.json ./
RUN npm install --omit=dev && chown -R node:node /app

COPY --chown=node:node . .

USER node

EXPOSE 3000

CMD ["node", "src/server.js"]
