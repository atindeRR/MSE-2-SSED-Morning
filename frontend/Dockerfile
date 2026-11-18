# MSE-2 | TaskFlow frontend (React + Vite, served by Nginx)
# Multi-stage build: stage 1 compiles the app, stage 2 ships only the static files.

# ---------- Stage 1: build the React application ----------
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies first (cached layer). devDependencies are needed here
# because Vite and the React plugin are build tools.
COPY package*.json ./
RUN npm install && npm cache clean --force

# Copy the source code and create the production build in /app/dist
COPY . .
RUN npm run build

# ---------- Stage 2: serve the build with Nginx ----------
FROM nginx:1.30-alpine

# Provided Nginx config: serves the React app and proxies /api and /health to backend:3000
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy only the compiled static files from stage 1 (no Node.js, no node_modules, no source code)
COPY --from=build /app/dist /usr/share/nginx/html

# Nginx listens on port 80 inside the container
EXPOSE 80

# Keep Nginx in the foreground so the container stays running
CMD ["nginx", "-g", "daemon off;"]
