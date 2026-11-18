FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

COPY package*.json ./

RUN npm install --omit=dev --no-audit --no-fund

COPY --chown=node:node src ./src
COPY --chown=node:node db ./db

USER node

EXPOSE 3000

CMD ["npm", "start"]
