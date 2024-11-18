FROM ubuntu:24.04 as builder



RUN apt update \
    && apt upgrade -y \
    && apt install -y libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev wget git gcc make libbrotli-dev

WORKDIR /app
RUN wget https://nginx.org/download/nginx-1.27.2.tar.gz && tar -zxf nginx-1.27.2.tar.gz
RUN git clone --recurse-submodules -j8 https://github.com/google/ngx_brotli
RUN cd nginx-1.27.2 && ./configure --with-compat --add-dynamic-module=../ngx_brotli \
    && make modules

FROM nginx:1.27.2

COPY ./compose/production/nginx/teapot.codes.pem /etc/nginx/teapot.codes.pem
COPY ./compose/production/nginx/teapot.codes.key /etc/nginx/teapot.codes.key
COPY ./compose/production/nginx/cloudflare.crt /etc/nginx/cloudflare.crt
COPY ./compose/production/nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /app/nginx-1.27.2/objs/ngx_http_brotli_static_module.so /etc/nginx/modules/
COPY --from=builder /app/nginx-1.27.2/objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/


