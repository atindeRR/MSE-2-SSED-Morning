FROM node:20.18-alpine3.20

ENV NODE_ENV=production
WORKDIR /app

# Install dependencies first so this layer is cached until package.json changes
COPY package.json ./
RUN npm install --omit=dev && npm cache clean --force

# Application source (owned by the unprivileged "node" user)
COPY --chown=1000:1000 src ./src

# uid 1000 is the unprivileged "node" user of the base image
USER 1000

# Default port; the real value comes from the PORT environment variable
EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=3s --start-period=30s --retries=5 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]

CMD ["node", "src/server.js"]
