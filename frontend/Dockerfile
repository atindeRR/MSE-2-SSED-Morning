
# Stage 1: Build the React application
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first for dependency caching
COPY package.json ./

RUN npm install

# Copy source code and create production build
COPY . .

RUN npm run build

# Stage 2: Serve the production build with Nginx
FROM nginx:alpine

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the provided reverse proxy configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
