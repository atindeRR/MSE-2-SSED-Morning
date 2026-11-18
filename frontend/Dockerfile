
# Stage 1: Build React application
FROM node:22-alpine AS build

WORKDIR /app

# Copy package configuration
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source
COPY . .

# Build production application
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
