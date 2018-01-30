FROM ubuntu:latest
MAINTAINER Olivier Cervello "olivier.cervello@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential redis-server git
ADD ./nginx.conf /etc/nginx/conf.d/
COPY . /var/www/scrapez
WORKDIR /var/www/scrapez
RUN pip install -r requirements.txt
