FROM node:22-alpine
ENV NODE_ENV=production
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY src/ ./src/
USER 1000:1000
EXPOSE 3000
CMD ["node", "src/server.js"]
