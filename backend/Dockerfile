FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --chown=1000:1000 package*.json ./
RUN npm install --omit=dev
COPY --chown=1000:1000 . .
EXPOSE 3000
USER 1000
CMD ["node", "src/server.js"]
