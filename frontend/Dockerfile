
# Stage 1: Build React application
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first for dependency caching
COPY package*.json ./

RUN npm install

# Copy frontend source code
COPY . .

# Create production build
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:1.27-alpine

# Copy production files
COPY --from=build /app/dist /usr/share/nginx/html

# Configure Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
