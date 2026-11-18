# ── Stage 1: Build ───────────────────────────────────────────────────────────
FROM node:22-alpine AS builder

WORKDIR /app

# Copy dependency manifests first for better layer caching
COPY package.json package-lock.json* ./

# Install ALL dependencies (dev included) needed for the Vite build
RUN npm ci

# Copy the rest of the source
COPY . .

# Produce the production static bundle → /app/dist
RUN npm run build

# ── Stage 2: Serve ───────────────────────────────────────────────────────────
FROM nginx:alpine AS runner

# Remove the default nginx placeholder page
RUN rm -rf /usr/share/nginx/html/*

# Copy the compiled React/Vite output from the builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy the project's nginx reverse-proxy config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
