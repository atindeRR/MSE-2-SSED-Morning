FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package*.json ./

RUN npm install --omit=dev

COPY --chown=node:node src ./src

USER 1000:1000

EXPOSE 3000

CMD ["npm", "start"]
