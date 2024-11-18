FROM valkey/valkey:latest

COPY ./compose/production/valkey/valkey.conf ./valkey.conf

CMD ["valkey-server", "./valkey.conf"]
