FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package.json ./

RUN npm install --omit=dev && npm cache clean --force

COPY src/ ./src/

USER 1000:1000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["wget", "-q", "-O", "-", "http://127.0.0.1:3000/health"]

CMD ["node", "src/server.js"]
