FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/
RUN mkdir /mysite
RUN mkdir /mysite/static
RUN mkdir /mysite/media