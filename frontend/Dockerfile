# syntax=docker/dockerfile:1

# ---------- Stage 1: build the React application ----------
FROM node:20-alpine AS build
WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY index.html vite.config.js ./
COPY src ./src
RUN npm run build

# ---------- Stage 2: serve the production build with Nginx ----------
FROM nginx:1.27-alpine AS production

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
