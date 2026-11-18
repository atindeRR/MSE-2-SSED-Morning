# Stage 1: Build the React application
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source code and build the app
COPY . .
RUN npm run build

# Stage 2: Serve the production build using Nginx
FROM nginx:alpine

# Copy the built assets from the builder stage to Nginx's default HTML folder
# Note: Vite builds to the 'dist' folder by default
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose the appropriate container port
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]