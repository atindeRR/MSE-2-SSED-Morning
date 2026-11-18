FROM node:22-alpine

ENV NODE_ENV=production

WORKDIR /app

COPY --chown=node:node package*.json ./
RUN npm install --omit=dev --no-audit --no-fund

COPY --chown=node:node src ./src

USER 1000:1000

EXPOSE 3000

CMD ["npm", "start"]
