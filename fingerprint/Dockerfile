FROM python:latest
MAINTAINER Team 2

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

#start the server
CMD python3 -m swagger_server

