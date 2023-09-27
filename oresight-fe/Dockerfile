# build environment
FROM node:19.9.0-alpine as build
WORKDIR /app

# Declare a default build argument
ARG ENV=production

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy the rest of the codebase
COPY . .

# Use the ENV argument to build the Angular app
RUN ENV=$ENV npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]