from flask import Flask, jsonify, make_response, request, render_template, Response
from pymongo import MongoClient
from pprint import pprint
import os
from flask_cors import CORS, cross_origin
from functools import wraps
from models import Evento, Lugar, Ponente

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

from dotenv import load_dotenv
SECRET_KEY = os.getenv("HOOK_SECRET")

connection = MongoClient(
        host='change_maker_db',
        port=27017
        )
db = connection['channge-maker-db']

def validate_secret(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        secret = request.headers.get('secret')
        if secret != SECRET_KEY:
            print('Invalid token -> Rejecting request')
            return make_response({"error" : "Invalid request token"})

        return func(*args, **kwargs)
    return decorated

def validate_request(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        request_type = request.json.get('type')
        supported_types = ['Entry', 'DeletedEntry']
        content_type = request.json.get('contentType')
        supported_content_types = ['evento', 'lugar', 'ponente']
        # Validate request type to be Entry or Deleted Entry
        if not request_type or request_type not in supported_types:
            return make_response({'warning' : f'No handler defined for request type {request_type}'})
        # Validate request type to be an accepted type
        if not content_type or content_type not in supported_content_types:
            return make_response({'warning' : f'No handler defined for content type {content_type}'})

        return func(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET'])
def root():
    return 'Change Maker API for CMS '

@app.route('/hooks', methods=['POST'])
@validate_secret
def hooks_handler():
    req = request.json
    type = req.get('type')
    if type == 'Entry':
        if insert_document(req):
            return make_response({'success' : 'added entry'}, 200)
        else:
            return make_response({'warn' : 'entry already added'}, 400)
    elif type == 'DeletedEntry':
        delete_document(req)
    else:
        return make_response({'error' : 'Invalid type of action'}, 400)

    return make_response({'ok' : 'ok'}, 200)

def insert_document(req):
    entryId = req['id']
    data = req['data']
    data.update({'entryId' : entryId})
    contentType = req.get('contentType')
    collection = db[contentType]

    entry = collection.find_one({'entryId' : entryId})
    if entry:
        collection.replace_one({'entryId' : entryId} , data)
    else:
        collection.insert_one(req['data'])

    return True
    
def delete_document(req: dict):
    entryId = req['id']
    contentType = req.get('contentType')
    collection = db[contentType]

    collection.delete_one({'entryId' : entryId})

    return True
    


app.run('0.0.0.0', '8080', debug=True)
