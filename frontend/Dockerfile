
# Stage 1: Build React application
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install --no-audit --no-fund \
    && npm cache clean --force

COPY . .

RUN npm run build

# Stage 2: Serve application with Nginx
FROM nginx:1.27-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
