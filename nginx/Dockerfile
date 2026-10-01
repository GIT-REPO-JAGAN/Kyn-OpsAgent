FROM nginx:1.29-alpine

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD wget --quiet --tries=1 --spider http://127.0.0.1:8080/nginx-health || exit 1

CMD ["nginx", "-g", "daemon off;"]
