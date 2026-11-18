
# Stage 1: Build the React application
FROM node:20-alpine AS build

WORKDIR /app

# Copy dependency configuration
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY . .

# Generate production build
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

# Copy production build
COPY --from=build /app/dist /usr/share/nginx/html

# Use the provided Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose Nginx port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
