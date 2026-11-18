FROM node:20-alpine
WORKDIR /app
COPY --chown=1000:1000 package*.json ./
RUN npm install --omit=dev
COPY --chown=1000:1000 src ./src
COPY --chown=1000:1000 db ./db
EXPOSE 3000
USER 1000
CMD ["node", "src/server.js"]
