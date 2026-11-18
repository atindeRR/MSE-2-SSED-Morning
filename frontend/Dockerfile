# syntax=docker/dockerfile:1

# ---- build: compile the React app with Vite ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---- runtime: serve static files with nginx ----
FROM nginx:1.27-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=5 \
  CMD ["/bin/sh", "-c", "wget -qO- http://127.0.0.1/ > /dev/null || exit 1"]

CMD ["nginx", "-g", "daemon off;"]
