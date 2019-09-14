FROM python:3-buster

RUN pip3 install Flask gunicorn

ADD . /app
WORKDIR /app

ENTRYPOINT ["gunicorn"]
