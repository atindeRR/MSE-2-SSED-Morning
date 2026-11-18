FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production \
    PORT=3000

COPY package*.json ./

RUN npm ci --omit=dev && npm cache clean --force

COPY --chown=1000:1000 . .

USER 1000

EXPOSE 3000

CMD ["npm", "start"]
