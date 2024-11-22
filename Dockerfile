FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN mkdir -p js css docs assets/images assets/json

COPY frontend/src/*.html .
COPY frontend/src/js/*.js ./js
COPY frontend/src/css/*.css ./css
COPY assets/json/* ./assets/json
COPY assets/images/* ./assets/images
# COPY docs/Doku.md ./docs

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
