FROM node:20-alpine3.20
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY --chown=node:node src ./src
COPY --chown=node:node db ./db
EXPOSE 3000
USER 1000:1000
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD [ "wget", "-q", "-O", "/dev/null", "http://127.0.0.1:3000/health" ]
CMD ["node", "src/server.js"]
