FROM redis:alpine3.21

WORKDIR /redis_config

COPY redis.conf /redis_config/redis.conf

EXPOSE 6379

CMD ["redis-server", "/redis_config/redis.conf"]