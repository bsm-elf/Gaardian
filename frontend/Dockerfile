# Stage 1: Build React App
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React app
RUN npm run build

# Stage 2: Serve with NGINX
FROM nginx:alpine

# Copy the built files to the NGINX html folder
COPY --from=build /app/build /usr/share/nginx/html

# Copy NGINX configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the logo file to the appropriate location in the NGINX container
COPY src/Gaardian.png /usr/share/nginx/html/

EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]
