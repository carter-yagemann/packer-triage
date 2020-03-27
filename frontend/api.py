#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Carter Yagemann
#
# This file is part of packer-triage.
#
# packer-triage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# packer-triage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with packer-triage.  If not, see <https://www.gnu.org/licenses/>.

import base64
from flask import *
from hashlib import sha256
import json
import os
import pymongo
import sys
import tasks

app = Flask('packer-triage')
app.mongo = pymongo.MongoClient('mongodb://mongo:%s@%s' % (
        os.environ['MONGO_PASS'], os.environ['MONGO_ADDRESS']))

##################
### LATEST API ###
##################

@app.route('/api/submit', methods=['POST'])
def submit():
    """Submit a sample for analysis"""
    return submit_v1()

@app.route('/api/results/<_hash>', methods=['GET'])
def results(_hash):
    """Get results for a sample"""
    return results_v1(_hash)

#####################
### API VERSION 1 ###
#####################

@app.route('/api/v1/submit', methods=['POST'])
def submit_v1():
    """Submit a sample for analysis, API v1"""
    if 'file' not in request.files:
        res = {'response': {'code': 2, 'description': 'No file in request'}}
        return json.dumps(res), 400

    _file = request.files['file']
    file_data = _file.read()
    _hash = sha256(file_data).hexdigest()

    # submit copy for work
    file_data_encoded = base64.b64encode(file_data).decode("ascii")
    tasks.get_prediction.delay(_hash, file_data_encoded)

    # include hash in response so there's no ambiguity on what to
    # request when querying /results
    res = {'response': {'code': 0, 'description': 'OK'},
           'data': _hash}

    return json.dumps(res), 200

@app.route('/api/v1/results/<_hash>', methods=['GET'])
def results_v1(_hash):
    """Get results for a sample, API v1"""
    # Result should be a json that looks something like:
    #
    #     {'response': {'code': 0, 'description': 'OK'},
    #       'data': {
    #         'hash': '...'  # the sample's hash (used to locate records)
    #         'label': 'foo',  # tl;dr, what should this sample be treated as (packed, unpacked, UPX, etc.)
    #         'is_packed': {'yes': 0.2, 'no': 0.8},               # binary classification
    #         'packer': {'upx': 0.912, 'pecompact': 0.0001, ...}  # multi-class
    #         'first_scan': 1568470824,  # UNIX epoch
    #         'latest_scan': 1568470824,
    #       }
    #     }
    #
    # Note, we plan to store JSON objects in a NoSQL database,
    # so for the frontend it should be as simple as slapping
    # the database query result into 'data'.

    try:
        record = app.mongo['packertriage']['results'].find_one({'hash': _hash})
    except pymongo.errors.ServerSelectionTimeoutError:
        res = {'response': {'code': 1, 'description': 'Internal Server Error'}}
        return json.dumps(res), 500

    if record is None:
        res = {'response': {'code': 2, 'description': 'Result not found'}}
    else:
        del record['_id']
        res = {'response': {'code': 0, 'description': 'OK'},
               'data': record}

    return json.dumps(res), 200
