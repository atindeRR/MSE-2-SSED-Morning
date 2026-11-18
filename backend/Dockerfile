FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY --chown=1000:1000 package*.json ./
RUN npm install --omit=dev --no-audit --no-fund && npm cache clean --force

COPY --chown=1000:1000 src ./src

USER 1000:1000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 CMD ["node", "-e", "fetch('http://127.0.0.1:' + (process.env.PORT || 3000) + '/health').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"]

CMD ["node", "src/server.js"]
