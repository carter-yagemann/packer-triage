FROM python:3-buster

RUN pip3 install Flask gunicorn pymongo

ADD . /app
RUN pip install -r /app/worker/requirements.txt
WORKDIR /app

ENTRYPOINT ["/bin/bash"]
