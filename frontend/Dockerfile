FROM python:3-buster

RUN pip3 install Flask gunicorn pymongo

ADD . /app
WORKDIR /app

ENTRYPOINT ["gunicorn"]
