FROM nginx:latest

RUN rm /etc/nginx/conf.b/default.conf
COPY nginx.conf /etc/nginx/conf.b
COPY proxy_params /etc/nginx
