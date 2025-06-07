FROM nginx:alpine3.21-slim

WORKDIR /nginx_config

COPY nginx.conf /nginx_config/nginx.conf

EXPOSE 443

CMD ["nginx", "-c", "/nginx_config/nginx.conf", "-g", "daemon off;"]