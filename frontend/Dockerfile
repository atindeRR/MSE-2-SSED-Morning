# ---- Stage 1: Build ----
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

# ---- Stage 2: Serve with Nginx ----
FROM nginx:1.27-alpine
# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*
# Copy the production build from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html
# Use our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose port 80
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
