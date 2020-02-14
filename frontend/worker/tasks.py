from celery import Celery
from hashlib import sha256
#from modeling import model
from unittest.mock import MagicMock
import tempfile
import json
import os

class Persistor:
    def __init__(self, config):
        self.dict = {}

    def store(self, key, value):
        self.dict[key] = value

    def retrieve(self, key):
        return self.dict.get(key, None)

rabbit_addr = os.environ["RABBITMQ_ADDRESS"]
if rabbit_addr == "local":
    rabbit_addr = "rabbit:9002"


mongo_addr = os.environ["MONGO_ADDRESS"]
if mongo_addr == "local":
    mongo_addr = "mongo:27017"
    

# app = Celery('tasks', broker="amqp://rabbit:vC28hkTLeMVvTYwuPVEvvIBYMhtGMXX+uZ1D8wCsklA=@127.0.0.1:9002//")
app = Celery('tasks', broker=("amqp://rabbit:%s@%s//" % (os.environ["RABBITMQ_DEFAULT_PASS"], rabbit_addr)), backend=("mongodb://mongo:%s@%s//" % (os.environ["MONGO_PASS"], mongo_addr)))

# mock model
model = MagicMock()
model.predict = MagicMock(return_value={'packer': 'upx'})

# must change the tag part
@app.task
def get_prediction(_hash, _bytes):
    tag = "2019-07-26T151222.003216_model_1902_per_class_5_classes_12_epochs"
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(_bytes)
        res = model.predict(tmp.name, tag)
    # persistor.store(_hash, res)
    return res

