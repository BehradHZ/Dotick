FROM node:24.19.0-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps/client/package.json apps/client/package.json
RUN npm ci --no-audit --no-fund
COPY apps/client apps/client
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.28.0-alpine AS runtime
COPY --from=build /app/apps/client/dist /usr/share/nginx/html
EXPOSE 8080
