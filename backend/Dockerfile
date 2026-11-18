FROM node:20-alpine

WORKDIR /app

ENV PORT=3000

COPY --chown=1000:1000 package.json ./

RUN npm install --omit=dev \
    && chown -R 1000:1000 /app

COPY --chown=1000:1000 src ./src
COPY --chown=1000:1000 db ./db

USER 1000

EXPOSE 3000

CMD ["npm", "start"]
