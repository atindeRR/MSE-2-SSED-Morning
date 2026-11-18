# ---- Stage 1: build the React (Vite) app ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ---- Stage 2: serve the static build with Nginx ----
FROM nginx:1.27-alpine
# nginx.conf serves the SPA and proxies /api + /health to the "backend" service
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
