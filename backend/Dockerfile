FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev && npm cache clean --force
COPY src ./src
ENV NODE_ENV=production
EXPOSE 3000
USER 1000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 CMD ["node", "-e", "fetch('http://127.0.0.1:3000/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
CMD ["node", "src/server.js"]
