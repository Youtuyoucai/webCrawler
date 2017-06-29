FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf

RUN echo "America/Los_Angeles" > /etc/timezone

RUN dpkg-reconfigure -f noninteractive tzdata