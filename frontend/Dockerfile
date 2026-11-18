# ─────────────────────────────────────────────
# Stage 1 – Build
# ─────────────────────────────────────────────
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency manifests first for better layer caching.
# package-lock.json is copied only when it exists (wildcard handles absence).
COPY package.json package-lock.json* ./

# Install all dependencies (including devDependencies needed for the build).
RUN npm install

# Copy the rest of the frontend source code.
COPY . .

# Build the React/Vite application – output lands in /app/dist
RUN npm run build

# ─────────────────────────────────────────────
# Stage 2 – Production
# ─────────────────────────────────────────────
FROM nginx:alpine

# Copy the compiled static assets into Nginx's default web root.
COPY --from=build /app/dist /usr/share/nginx/html

# Replace the default Nginx config with our custom one.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port.
EXPOSE 80

# nginx:alpine's default CMD starts the server – no override needed.
