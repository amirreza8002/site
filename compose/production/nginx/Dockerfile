FROM docker.io/nginx:latest
COPY ./compose/production/nginx/cert.pem /etc/nginx/cert.pem
COPY ./compose/production/nginx/key.pem /etc/nginx/key.pem
COPY ./compose/production/nginx/cloudflare.crt /etc/nginx/cloudflare.crt
COPY ./compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
