FROM python:3.7-buster

RUN pip3 install Flask gunicorn pymongo

ADD ./requirements /app
RUN pip install -r /app/requirements.txt

ADD . /app
WORKDIR /app

ENTRYPOINT ["/bin/bash", "-c"]
