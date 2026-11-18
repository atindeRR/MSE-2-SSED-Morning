FROM node:22-alpine

WORKDIR /app

COPY package.json ./

RUN npm install --omit=dev --no-audit --no-fund

COPY --chown=node:node . .

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 CMD node -e "const h=require('node:http');const r=h.get({host:'127.0.0.1',port:3000,path:'/health'},s=>process.exit(s.statusCode===200?0:1));r.on('error',()=>process.exit(1))"

CMD ["npm", "start"]
