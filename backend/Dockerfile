FROM node:22-alpine

ENV NODE_ENV=production

WORKDIR /app

COPY package*.json ./
RUN npm install --omit=dev --no-audit --no-fund \
    && npm cache clean --force

COPY --chown=1000:1000 src ./src

USER 1000:1000

EXPOSE 3000

CMD ["node", "src/server.js"]
