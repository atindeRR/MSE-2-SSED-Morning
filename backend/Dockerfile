
FROM node:22-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --omit=dev --no-audit --no-fund

COPY --chown=node:node . .

ENV NODE_ENV=production

EXPOSE 3000

USER node

CMD ["npm", "start"]
