
FROM node:20-alpine

ENV NODE_ENV=production
WORKDIR /app

COPY package*.json ./

RUN npm install --omit=dev --no-audit --no-fund

COPY --chown=node:node . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
