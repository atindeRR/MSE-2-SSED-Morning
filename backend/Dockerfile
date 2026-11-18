FROM node:20.18.1-alpine3.20
ENV NODE_ENV=production
ENV PORT=3000
WORKDIR /app

# Copy dependency files first so this layer is cached
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force

COPY . .

USER 1000
EXPOSE 3000
HEALTHCHECK --interval=10s --timeout=3s --start-period=20s --retries=5 \
  CMD ["wget", "-qO", "/dev/null", "http://127.0.0.1:3000/health"]

CMD ["npm", "start"]
