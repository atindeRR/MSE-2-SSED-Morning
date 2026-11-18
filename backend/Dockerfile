FROM node:20.18.1-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev
COPY . .
EXPOSE 3000
USER node
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD wget -qO /dev/null http://127.0.0.1:3000/health || exit 1
CMD ["node", "src/server.js"]
