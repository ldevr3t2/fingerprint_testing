FROM ubuntu:latest
MAINTAINER Team 2
RUN apt-get update && apt-get install -y \
	git \
	python3.5 \
	python3-pip
#update pip
RUN pip3 install --upgrade pip
RUN apt-get install -y python-pip python-dev build-essential

#download flask-server
RUN pip3 install Flask-API
RUN pip install Flask-API
RUN pip3 install flask
RUN pip3 install markdown
RUN pip3 install requests
RUN pip install requests==1.1.0


COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

#start the server
CMD python3 -m swagger_server

