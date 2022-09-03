FROM python:3.10.0-slim-buster
ENV LANG C.UTF-8

RUN apt-get -y update && apt-get -y autoremove

RUN mkdir /app
WORKDIR /app

RUN apt-get install -y python python-pip python-dev

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app

EXPOSE 8000

COPY start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start