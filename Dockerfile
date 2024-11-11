FROM nginx:alpine

WORKDIR /usr/share/nginx/html

RUN mkdir -p js css project_information assets/images assets/json

COPY src/*.html .
COPY src/js/*.js ./js
COPY src/css/*.css ./css
COPY assets/json/* ./assets/json
COPY assets/images/* ./assets/images
COPY project_information/Doku.md ./project_information

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
