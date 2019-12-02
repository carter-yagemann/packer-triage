from __future__ import absolute_import
from celery import Celery
import model

app = Celery('tasks', broker="amqp://rabbit:oG3NEwTCv5oEGHoVS5AE8YwyYCwQqTgABCFDLL7czgc=@127.0.0.1:9002//")


@app.task(name='mytasks.getPrediction')
def getPrediction():
    tag = "2019-07-26T151222.003216_model_1902_per_class_5_classes_12_epochs"
    filepath = "../test/samples/"
    model.predict(filepath, tag)
