# Stage 1: Build React application
FROM node:20-alpine3.20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve production assets with Nginx
FROM nginx:1.27.2-alpine3.20
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD [ "wget", "-q", "-O", "/dev/null", "http://127.0.0.1:80/" ]
CMD ["nginx", "-g", "daemon off;"]
