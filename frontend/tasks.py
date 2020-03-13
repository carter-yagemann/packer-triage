from celery import Celery
from modeling import model
import tempfile
import pymongo
import json
import os
import base64


class Persistor:
    def __init__(self):
        self.mongo = pymongo.MongoClient('mongodb://mongo:%s@%s' % (os.environ['MONGO_PASS'], os.environ['MONGO_ADDRESS']))
        self.database = self.mongo['packertriage']
        self.collection = self.database['results']

    def store(self, _hash, res):
        # remove this remove statement later
        self.collection.remove({})
        self.collection.insert({'hash': _hash, 'result': res})

    def retrieve(self, _hash):
        return self.collection.find_one({'hash': _hash})

app = Celery('tasks', broker=("amqp://rabbit:%s@%s//" % (
        os.environ["RABBITMQ_DEFAULT_PASS"], os.environ["RABBITMQ_ADDRESS"])))


@app.task
def get_prediction(_hash, file_data):
    persistor = Persistor()
    
    byte = base64.b64decode(file_data)

    temp = tempfile.TemporaryFile()
    res = None
    with tempfile.NamedTemporaryFile(dir='../samples') as temp:
        temp.write(byte)
        tag = os.environ['MODEL_NAME']
        model_file_path = "/models"
        data_file_path = "/samples"
        res = model.predict(model_file_path, data_file_path, tag)
    # put the name of the packer and all the probabilities in a dict
    # figure out if the result produced is actually accurate
    # pull request
    print(res)
    persistor.store(_hash, res)
